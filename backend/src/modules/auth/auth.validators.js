'use strict';

const Joi = require('joi');

const signup = Joi.object({
  name: Joi.string().min(2).max(80).required(),
  email: Joi.string().email().required(),
  phone: Joi.string().pattern(/^\+?[0-9]{8,15}$/).optional(),
  password: Joi.string().min(8).max(128).required(),
  language: Joi.string().lowercase().length(2).default('en'),
});

const login = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).max(128).required(),
});

const refresh = Joi.object({
  refreshToken: Joi.string().required(),
});

const otpRequest = Joi.object({
  channel: Joi.string().valid('sms', 'email').required(),
  target: Joi.string().required(),
});

const otpVerify = Joi.object({
  channel: Joi.string().valid('sms', 'email').required(),
  target: Joi.string().required(),
  code: Joi.string().length(6).pattern(/^[0-9]{6}$/).required(),
});

const oauth = Joi.object({
  provider: Joi.string().valid('google', 'apple').required(),
  idToken: Joi.string().required(),
});

const forgot = Joi.object({
  email: Joi.string().email().required(),
});

const reset = Joi.object({
  token: Joi.string().required(),
  password: Joi.string().min(8).max(128).required(),
});

module.exports = { signup, login, refresh, otpRequest, otpVerify, oauth, forgot, reset };
