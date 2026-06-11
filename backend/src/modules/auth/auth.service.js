'use strict';

const bcrypt = require('bcrypt');
const { v4: uuid } = require('uuid');
const db = require('../../config/db');
const redis = require('../../config/redis');
const { issueTokens, verifyRefresh } = require('../../utils/jwt');
const { randomToken } = require('../../utils/crypto');
const { sendOtp, verifyOtp } = require('../../utils/otp');
const { HttpError } = require('../../middleware/error');

const BCRYPT_ROUNDS = 12;

const safeUser = (row) => ({
  id: row.id,
  name: row.name,
  email: row.email,
  phone: row.phone,
  language: row.language,
  subscription_plan: row.subscription_plan,
  email_verified: row.email_verified,
  phone_verified: row.phone_verified,
  avatar_url: row.avatar_url,
  created_at: row.created_at,
});

const findByEmail = async (email) => {
  const { rows } = await db.query('SELECT * FROM users WHERE lower(email) = lower($1) LIMIT 1', [email]);
  return rows[0] || null;
};

const findById = async (id) => {
  const { rows } = await db.query('SELECT * FROM users WHERE id = $1 LIMIT 1', [id]);
  return rows[0] || null;
};

const signup = async ({ name, email, phone, password, language }) => {
  const existing = await findByEmail(email);
  if (existing) throw new HttpError(409, 'An account with this email already exists');
  const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);
  const id = uuid();
  const { rows } = await db.query(
    `INSERT INTO users (id, name, email, phone, password_hash, language, subscription_plan)
     VALUES ($1, $2, $3, $4, $5, $6, 'free')
     RETURNING *`,
    [id, name, email.toLowerCase(), phone || null, hash, language]
  );
  const user = rows[0];
  return { user: safeUser(user), tokens: issueTokens(user) };
};

const login = async ({ email, password }) => {
  const user = await findByEmail(email);
  if (!user || !user.password_hash) throw new HttpError(401, 'Invalid email or password');
  const ok = await bcrypt.compare(password, user.password_hash);
  if (!ok) throw new HttpError(401, 'Invalid email or password');
  await db.query('UPDATE users SET last_login_at = NOW() WHERE id = $1', [user.id]);
  return { user: safeUser(user), tokens: issueTokens(user) };
};

const refresh = async ({ refreshToken }) => {
  let payload;
  try {
    payload = verifyRefresh(refreshToken);
  } catch (_) {
    throw new HttpError(401, 'Invalid refresh token');
  }
  const user = await findById(payload.sub);
  if (!user) throw new HttpError(401, 'User no longer exists');
  return { user: safeUser(user), tokens: issueTokens(user) };
};

const requestOtp = async ({ channel, target }) => sendOtp({ channel, target });

const verifyOtpAndUpgrade = async ({ channel, target, code, userId }) => {
  const ok = await verifyOtp({ channel, target, code });
  if (!ok) throw new HttpError(400, 'Invalid or expired OTP');
  if (userId) {
    const field = channel === 'sms' ? 'phone_verified' : 'email_verified';
    await db.query(`UPDATE users SET ${field} = TRUE WHERE id = $1`, [userId]);
  }
  return { verified: true };
};

const oauthSignIn = async ({ provider, idToken: _idToken }) => {
  throw new HttpError(
    501,
    `OAuth (${provider}) verification is stubbed; wire up google-auth-library / apple-signin-auth in production.`
  );
};

const forgot = async ({ email }) => {
  const user = await findByEmail(email);
  if (!user) return { ok: true };
  const token = randomToken(24);
  await redis.set(`pwreset:${token}`, user.id, 'EX', 60 * 30);
  return { ok: true, devToken: process.env.NODE_ENV === 'production' ? undefined : token };
};

const reset = async ({ token, password }) => {
  const userId = await redis.get(`pwreset:${token}`);
  if (!userId) throw new HttpError(400, 'Invalid or expired reset token');
  const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);
  await db.query('UPDATE users SET password_hash = $1 WHERE id = $2', [hash, userId]);
  await redis.del(`pwreset:${token}`);
  return { ok: true };
};

module.exports = {
  signup,
  login,
  refresh,
  requestOtp,
  verifyOtpAndUpgrade,
  oauthSignIn,
  forgot,
  reset,
  findById,
  safeUser,
};
