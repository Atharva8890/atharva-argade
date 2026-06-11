'use strict';

const { verifyAccess } = require('../utils/jwt');
const { HttpError } = require('./error');

const requireAuth = (req, _res, next) => {
  const header = req.headers.authorization || '';
  const [scheme, token] = header.split(' ');
  if (scheme !== 'Bearer' || !token) {
    return next(new HttpError(401, 'Missing or invalid Authorization header'));
  }
  try {
    const payload = verifyAccess(token);
    req.user = { id: payload.sub, email: payload.email, plan: payload.plan };
    return next();
  } catch (err) {
    return next(new HttpError(401, 'Invalid or expired token'));
  }
};

const requirePlan = (...allowed) => (req, _res, next) => {
  if (!req.user) return next(new HttpError(401, 'Unauthenticated'));
  if (!allowed.includes(req.user.plan)) {
    return next(new HttpError(403, `Plan upgrade required: ${allowed.join(' or ')}`));
  }
  return next();
};

module.exports = { requireAuth, requirePlan };
