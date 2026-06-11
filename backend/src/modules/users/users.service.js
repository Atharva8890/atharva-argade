'use strict';

const db = require('../../config/db');
const { HttpError } = require('../../middleware/error');
const { safeUser } = require('../auth/auth.service');

const updateProfile = async (userId, patch) => {
  const allowed = ['name', 'phone', 'language', 'avatar_url'];
  const fields = [];
  const values = [];
  let i = 1;
  for (const key of allowed) {
    if (patch[key] !== undefined) {
      fields.push(`${key} = $${i++}`);
      values.push(patch[key]);
    }
  }
  if (!fields.length) throw new HttpError(400, 'No updatable fields supplied');
  values.push(userId);
  const { rows } = await db.query(
    `UPDATE users SET ${fields.join(', ')}, updated_at = NOW() WHERE id = $${i} RETURNING *`,
    values
  );
  if (!rows.length) throw new HttpError(404, 'User not found');
  return safeUser(rows[0]);
};

const listContacts = async (userId) => {
  const { rows } = await db.query(
    `SELECT c.id, c.contact_user_id, c.alias, c.created_at,
            u.name, u.email, u.phone, u.language, u.avatar_url
     FROM contacts c
     JOIN users u ON u.id = c.contact_user_id
     WHERE c.user_id = $1
     ORDER BY (c.alias, u.name) ASC`,
    [userId]
  );
  return rows;
};

const addContact = async (userId, { email, alias }) => {
  const { rows: targets } = await db.query('SELECT id FROM users WHERE lower(email) = lower($1)', [email]);
  if (!targets.length) throw new HttpError(404, 'No user found for that email');
  const contactId = targets[0].id;
  if (contactId === userId) throw new HttpError(400, 'Cannot add yourself as a contact');
  const { rows } = await db.query(
    `INSERT INTO contacts (user_id, contact_user_id, alias)
     VALUES ($1, $2, $3)
     ON CONFLICT (user_id, contact_user_id) DO UPDATE SET alias = EXCLUDED.alias
     RETURNING *`,
    [userId, contactId, alias || null]
  );
  return rows[0];
};

const removeContact = async (userId, contactUserId) => {
  await db.query('DELETE FROM contacts WHERE user_id = $1 AND contact_user_id = $2', [userId, contactUserId]);
  return { ok: true };
};

const deleteAccount = async (userId) => {
  await db.query('DELETE FROM users WHERE id = $1', [userId]);
  return { ok: true };
};

module.exports = { updateProfile, listContacts, addContact, removeContact, deleteAccount };
