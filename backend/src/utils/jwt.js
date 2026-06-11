'use strict';

const jwt = require('jsonwebtoken');
const config = require('../config');

const signAccess = (payload) =>
  jwt.sign(payload, config.jwt.accessSecret, {
    expiresIn: config.jwt.accessTtl,
    issuer: 'voicebridge-ai',
  });

const signRefresh = (payload) =>
  jwt.sign(payload, config.jwt.refreshSecret, {
    expiresIn: config.jwt.refreshTtl,
    issuer: 'voicebridge-ai',
  });

const verifyAccess = (token) => jwt.verify(token, config.jwt.accessSecret, { issuer: 'voicebridge-ai' });
const verifyRefresh = (token) => jwt.verify(token, config.jwt.refreshSecret, { issuer: 'voicebridge-ai' });

const issueTokens = (user) => {
  const payload = { sub: user.id, email: user.email, plan: user.subscription_plan };
  return {
    accessToken: signAccess(payload),
    refreshToken: signRefresh({ sub: user.id }),
    tokenType: 'Bearer',
    expiresIn: config.jwt.accessTtl,
  };
};

module.exports = { signAccess, signRefresh, verifyAccess, verifyRefresh, issueTokens };
