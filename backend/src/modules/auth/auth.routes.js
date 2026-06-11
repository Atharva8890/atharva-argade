'use strict';

const { Router } = require('express');
const ctrl = require('./auth.controller');
const v = require('./auth.validators');
const { validate } = require('../../middleware/validate');
const { requireAuth } = require('../../middleware/auth');
const { authLimiter } = require('../../middleware/rateLimit');

const router = Router();

router.use(authLimiter);

router.post('/signup', validate(v.signup), ctrl.signup);
router.post('/login', validate(v.login), ctrl.login);
router.post('/refresh', validate(v.refresh), ctrl.refresh);
router.post('/oauth', validate(v.oauth), ctrl.oauthSignIn);

router.post('/otp/request', validate(v.otpRequest), ctrl.requestOtp);
router.post('/otp/verify', validate(v.otpVerify), ctrl.verifyOtp);

router.post('/forgot-password', validate(v.forgot), ctrl.forgot);
router.post('/reset-password', validate(v.reset), ctrl.reset);

router.get('/me', requireAuth, ctrl.me);

module.exports = router;
