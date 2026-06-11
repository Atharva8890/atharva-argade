'use strict';

const { v4: uuid } = require('uuid');
const db = require('../../config/db');
const ai = require('../ai/ai.service');

const getOrCreateThread = async (userA, userB) => {
  const [a, b] = [userA, userB].sort();
  const { rows } = await db.query(
    `INSERT INTO chat_threads (id, user_a, user_b)
     VALUES ($1, $2, $3)
     ON CONFLICT (user_a, user_b) DO UPDATE SET updated_at = NOW()
     RETURNING *`,
    [uuid(), a, b]
  );
  return rows[0];
};

const listThreads = async (userId) => {
  const { rows } = await db.query(
    `SELECT t.*,
            u.id   AS peer_id,
            u.name AS peer_name,
            u.language AS peer_language,
            u.avatar_url AS peer_avatar,
            (SELECT json_build_object('text', m.text_original, 'created_at', m.created_at, 'sender_id', m.sender_id)
              FROM chat_messages m WHERE m.thread_id = t.id ORDER BY m.created_at DESC LIMIT 1) AS last_message
     FROM chat_threads t
     JOIN users u ON u.id = CASE WHEN t.user_a = $1 THEN t.user_b ELSE t.user_a END
     WHERE t.user_a = $1 OR t.user_b = $1
     ORDER BY t.updated_at DESC`,
    [userId]
  );
  return rows;
};

const listMessages = async (threadId, { limit = 50, before } = {}) => {
  const params = [threadId, limit];
  let where = 'WHERE thread_id = $1';
  if (before) {
    params.push(before);
    where += ` AND created_at < $${params.length}`;
  }
  const { rows } = await db.query(
    `SELECT * FROM chat_messages ${where} ORDER BY created_at DESC LIMIT $2`,
    params
  );
  return rows.reverse();
};

const sendMessage = async ({ threadId, senderId, text, type = 'text', mediaUrl, sourceLanguage, targetLanguage, autoTranslate = true }) => {
  let translated = null;
  if (autoTranslate && text && sourceLanguage && targetLanguage && sourceLanguage !== targetLanguage) {
    try {
      const r = await ai.translate({ text, source: sourceLanguage, target: targetLanguage });
      translated = r.text;
    } catch (_) {
      // Fail soft on translation errors
    }
  }
  const id = uuid();
  const { rows } = await db.query(
    `INSERT INTO chat_messages
       (id, thread_id, sender_id, type, text_original, text_translated,
        source_language, target_language, media_url)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
     RETURNING *`,
    [id, threadId, senderId, type, text || null, translated, sourceLanguage || null, targetLanguage || null, mediaUrl || null]
  );
  await db.query('UPDATE chat_threads SET updated_at = NOW() WHERE id = $1', [threadId]);
  return rows[0];
};

module.exports = { getOrCreateThread, listThreads, listMessages, sendMessage };
