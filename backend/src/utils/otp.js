'use strict';

const crypto = require('crypto');
const redis = require('../config/redis');
const logger = require('./logger');
const config = require('../config');

const OTP_TTL_SECONDS = 5 * 60;
const OTP_LENGTH = 6;

const generateCode = () => {
  const max = 10 ** OTP_LENGTH;
  return String(crypto.randomInt(0, max)).padStart(OTP_LENGTH, '0');
};

const key = (channel, target) => `otp:${channel}:${target.toLowerCase()}`;

const sendOtp = async ({ channel, target }) => {
  const code = generateCode();
  await redis.set(key(channel, target), code, 'EX', OTP_TTL_SECONDS);

  if (channel === 'sms' && config.otp.twilio.sid) {
    logger.info({ target }, 'Would send OTP via Twilio (configure axios call in production)');
  } else if (channel === 'email') {
    logger.info({ target }, 'Would send OTP via email');
  } else {
    logger.warn({ target, code }, 'No OTP provider configured - logging code for dev only');
  }

  return { ttl: OTP_TTL_SECONDS, devCode: process.env.NODE_ENV === 'production' ? undefined : code };
};

const verifyOtp = async ({ channel, target, code }) => {
  const stored = await redis.get(key(channel, target));
  if (!stored) return false;
  const ok = stored === String(code).trim();
  if (ok) await redis.del(key(channel, target));
  return ok;
};

module.exports = { sendOtp, verifyOtp };
