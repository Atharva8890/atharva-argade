'use strict';

const { v4: uuid } = require('uuid');
const db = require('../../config/db');
const { HttpError } = require('../../middleware/error');

const createCall = async (callerId, { receiverId, type = 'voice', isGroup = false, participants = [] }) => {
  const id = uuid();
  const allParticipants = isGroup
    ? Array.from(new Set([callerId, ...participants]))
    : [callerId, receiverId];

  if (allParticipants.length < 2) throw new HttpError(400, 'A call requires at least two participants');
  if (allParticipants.length > 20) throw new HttpError(400, 'Group calls are limited to 20 participants');

  await db.tx(async (client) => {
    await client.query(
      `INSERT INTO calls (id, caller_id, receiver_id, type, is_group, status, start_time)
       VALUES ($1, $2, $3, $4, $5, 'ringing', NOW())`,
      [id, callerId, isGroup ? null : receiverId, type, isGroup]
    );
    const values = allParticipants.map((_, i) => `($1, $${i + 2})`).join(',');
    await client.query(
      `INSERT INTO call_participants (call_id, user_id) VALUES ${values}
       ON CONFLICT DO NOTHING`,
      [id, ...allParticipants]
    );
  });

  return { id, status: 'ringing', participants: allParticipants };
};

const updateStatus = async (callId, status, extra = {}) => {
  const fields = ['status = $2'];
  const values = [callId, status];
  let i = 3;
  if (extra.endTime) {
    fields.push(`end_time = $${i++}`);
    values.push(extra.endTime);
  }
  if (extra.durationSec !== undefined) {
    fields.push(`duration_sec = $${i++}`);
    values.push(extra.durationSec);
  }
  if (extra.recordingUrl) {
    fields.push(`recording_url = $${i++}`);
    values.push(extra.recordingUrl);
  }
  const { rows } = await db.query(
    `UPDATE calls SET ${fields.join(', ')}, updated_at = NOW() WHERE id = $1 RETURNING *`,
    values
  );
  return rows[0] || null;
};

const endCall = async (callId) => {
  const { rows } = await db.query(
    `UPDATE calls
       SET status = 'ended',
           end_time = NOW(),
           duration_sec = EXTRACT(EPOCH FROM (NOW() - start_time))::int,
           updated_at = NOW()
     WHERE id = $1
     RETURNING *`,
    [callId]
  );
  return rows[0] || null;
};

const history = async (userId, { limit = 50, offset = 0 } = {}) => {
  const { rows } = await db.query(
    `SELECT c.*, ARRAY(
        SELECT json_build_object('user_id', cp.user_id, 'language', u.language, 'name', u.name)
        FROM call_participants cp
        JOIN users u ON u.id = cp.user_id
        WHERE cp.call_id = c.id
     ) AS participants
     FROM calls c
     WHERE c.id IN (SELECT call_id FROM call_participants WHERE user_id = $1)
     ORDER BY c.start_time DESC
     LIMIT $2 OFFSET $3`,
    [userId, limit, offset]
  );
  return rows;
};

const getCall = async (callId, userId) => {
  const { rows } = await db.query(
    `SELECT c.* FROM calls c
     WHERE c.id = $1
       AND c.id IN (SELECT call_id FROM call_participants WHERE user_id = $2)`,
    [callId, userId]
  );
  return rows[0] || null;
};

module.exports = { createCall, updateStatus, endCall, history, getCall };
