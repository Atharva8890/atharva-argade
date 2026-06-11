'use strict';

const { Router } = require('express');
const Joi = require('joi');
const service = require('./subscriptions.service');
const { requireAuth } = require('../../middleware/auth');
const { validate } = require('../../middleware/validate');

const router = Router();

router.get('/plans', (_req, res) => res.json({ plans: service.listPlans() }));

router.use(requireAuth);

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.get(
  '/me',
  wrap(async (req, res) => res.json({ subscription: await service.ofUser(req.user.id) }))
);

const orderSchema = Joi.object({
  plan: Joi.string().valid('premium', 'business').required(),
  gateway: Joi.string().valid('razorpay', 'stripe').default('razorpay'),
});

router.post(
  '/checkout',
  validate(orderSchema),
  wrap(async (req, res) => res.json(await service.createOrder(req.user.id, req.body)))
);

module.exports = router;
