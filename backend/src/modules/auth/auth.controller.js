'use strict';

const service = require('./auth.service');

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

const signup = wrap(async (req, res) => {
  const result = await service.signup(req.body);
  res.status(201).json(result);
});

const login = wrap(async (req, res) => {
  const result = await service.login(req.body);
  res.json(result);
});

const refresh = wrap(async (req, res) => {
  const result = await service.refresh(req.body);
  res.json(result);
});

const me = wrap(async (req, res) => {
  const user = await service.findById(req.user.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ user: service.safeUser(user) });
});

const requestOtp = wrap(async (req, res) => {
  const result = await service.requestOtp(req.body);
  res.json(result);
});

const verifyOtp = wrap(async (req, res) => {
  const result = await service.verifyOtpAndUpgrade({ ...req.body, userId: req.user?.id });
  res.json(result);
});

const oauthSignIn = wrap(async (req, res) => {
  const result = await service.oauthSignIn(req.body);
  res.json(result);
});

const forgot = wrap(async (req, res) => {
  const result = await service.forgot(req.body);
  res.json(result);
});

const reset = wrap(async (req, res) => {
  const result = await service.reset(req.body);
  res.json(result);
});

module.exports = { signup, login, refresh, me, requestOtp, verifyOtp, oauthSignIn, forgot, reset };
