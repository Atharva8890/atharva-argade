'use strict';

const rateLimit = require('express-rate-limit');
const config = require('../config');

const authLimiter = rateLimit({
  windowMs: 60_000,
  max: config.rateLimit.auth,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many auth requests, please try again later.' },
});

const apiLimiter = rateLimit({
  windowMs: 60_000,
  max: config.rateLimit.api,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please slow down.' },
});

module.exports = { authLimiter, apiLimiter };
