'use strict';

const crypto = require('crypto');
const config = require('../config');

const ALGO = 'aes-256-gcm';
const IV_LENGTH = 12;

const getKey = () => {
  const key = config.crypto.aesKey;
  if (!key) {
    return crypto.createHash('sha256').update('voicebridge-dev-key').digest();
  }
  if (key.length === 64) return Buffer.from(key, 'hex');
  try {
    const buf = Buffer.from(key, 'base64');
    if (buf.length === 32) return buf;
  } catch (_) {
    // fallthrough
  }
  return crypto.createHash('sha256').update(key).digest();
};

const encrypt = (plaintext) => {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGO, getKey(), iv);
  const enc = Buffer.concat([cipher.update(String(plaintext), 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, enc]).toString('base64');
};

const decrypt = (ciphertext) => {
  const data = Buffer.from(ciphertext, 'base64');
  const iv = data.subarray(0, IV_LENGTH);
  const tag = data.subarray(IV_LENGTH, IV_LENGTH + 16);
  const enc = data.subarray(IV_LENGTH + 16);
  const decipher = crypto.createDecipheriv(ALGO, getKey(), iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(enc), decipher.final()]).toString('utf8');
};

const sha256 = (input) => crypto.createHash('sha256').update(String(input)).digest('hex');

const randomToken = (bytes = 32) => crypto.randomBytes(bytes).toString('hex');

module.exports = { encrypt, decrypt, sha256, randomToken };
