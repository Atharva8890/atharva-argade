'use strict';

const { v4: uuid } = require('uuid');
const db = require('../../config/db');
const { randomToken } = require('../../utils/crypto');
const ai = require('../ai/ai.service');
const config = require('../../config');

const create = async (hostId, { title, scheduledAt, defaultLanguage = 'en' }) => {
  const id = uuid();
  const joinCode = randomToken(4).toUpperCase().slice(0, 8);
  const { rows } = await db.query(
    `INSERT INTO meetings (id, host_id, title, scheduled_at, default_language, join_code)
     VALUES ($1,$2,$3,$4,$5,$6) RETURNING *`,
    [id, hostId, title, scheduledAt || null, defaultLanguage, joinCode]
  );
  return rows[0];
};

const join = async (userId, { meetingId, joinCode, language }) => {
  const { rows } = await db.query(
    `SELECT * FROM meetings WHERE (id = $1 OR join_code = $2) LIMIT 1`,
    [meetingId || null, joinCode || null]
  );
  if (!rows.length) return null;
  const meeting = rows[0];
  await db.query(
    `INSERT INTO meeting_participants (meeting_id, user_id, language)
     VALUES ($1,$2,$3)
     ON CONFLICT (meeting_id, user_id) DO UPDATE SET language = EXCLUDED.language, joined_at = NOW()`,
    [meeting.id, userId, language || meeting.default_language]
  );
  return meeting;
};

const transcript = async (meetingId) => {
  const { rows } = await db.query(
    `SELECT * FROM meeting_segments WHERE meeting_id = $1 ORDER BY created_at ASC`,
    [meetingId]
  );
  return rows;
};

const generateSummary = async (meetingId) => {
  const segments = await transcript(meetingId);
  const transcriptText = segments.map((s) => `${s.speaker_name || s.speaker_id}: ${s.text_original}`).join('\n');
  if (!transcriptText.trim()) return { summary: 'No transcript available yet.' };

  if (!config.ai.openaiKey) {
    return { summary: '[OPENAI_API_KEY missing - summary disabled]', transcript: transcriptText };
  }

  const axios = require('axios');
  const { data } = await axios.post(
    'https://api.openai.com/v1/chat/completions',
    {
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'You produce concise meeting summaries with key decisions and action items.' },
        { role: 'user', content: `Summarize this meeting transcript:\n\n${transcriptText}` },
      ],
      temperature: 0.3,
    },
    { headers: { Authorization: `Bearer ${config.ai.openaiKey}` }, timeout: 30_000 }
  );
  const summary = data?.choices?.[0]?.message?.content?.trim() || '';
  await db.query('UPDATE meetings SET summary = $1, summary_generated_at = NOW() WHERE id = $2', [summary, meetingId]);
  return { summary, transcript: transcriptText };
};

module.exports = { create, join, transcript, generateSummary, ai };
