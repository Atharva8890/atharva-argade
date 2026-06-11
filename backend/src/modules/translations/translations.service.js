'use strict';

const { v4: uuid } = require('uuid');
const db = require('../../config/db');

const log = async ({
  callId,
  speakerId,
  sourceLanguage,
  targetLanguage,
  originalText,
  translatedText,
  audioUrl,
  provider,
  latencyMs,
}) => {
  const id = uuid();
  const { rows } = await db.query(
    `INSERT INTO translations
       (id, call_id, speaker_id, source_language, target_language, original_text, translated_text, audio_url, provider, latency_ms)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
     RETURNING *`,
    [id, callId, speakerId, sourceLanguage, targetLanguage, originalText, translatedText, audioUrl || null, provider || null, latencyMs || null]
  );
  return rows[0];
};

const transcript = async (callId) => {
  const { rows } = await db.query(
    `SELECT id, speaker_id, source_language, target_language, original_text, translated_text, created_at
     FROM translations
     WHERE call_id = $1
     ORDER BY created_at ASC`,
    [callId]
  );
  return rows;
};

const summary = async (callId) => {
  const { rows } = await db.query(
    `SELECT COUNT(*) AS segments,
            ARRAY_AGG(DISTINCT source_language) AS source_languages,
            ARRAY_AGG(DISTINCT target_language) AS target_languages,
            AVG(latency_ms)::int AS avg_latency_ms
     FROM translations WHERE call_id = $1`,
    [callId]
  );
  return rows[0];
};

module.exports = { log, transcript, summary };
