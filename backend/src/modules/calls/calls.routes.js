'use strict';

const { Router } = require('express');
const Joi = require('joi');
const service = require('./calls.service');
const { validate } = require('../../middleware/validate');
const { requireAuth } = require('../../middleware/auth');
const config = require('../../config');

const router = Router();
router.use(requireAuth);

const initiateSchema = Joi.object({
  receiverId: Joi.string().uuid(),
  type: Joi.string().valid('voice', 'video').default('voice'),
  isGroup: Joi.boolean().default(false),
  participants: Joi.array().items(Joi.string().uuid()).max(19).default([]),
}).custom((v, helpers) => {
  if (!v.isGroup && !v.receiverId) return helpers.error('any.custom', { message: 'receiverId required for 1:1 calls' });
  return v;
});

const endSchema = Joi.object({
  durationSec: Joi.number().integer().min(0).optional(),
  recordingUrl: Joi.string().uri().optional(),
});

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.get(
  '/ice-servers',
  wrap(async (_req, res) => res.json({ iceServers: config.webrtc.iceServers }))
);

router.post(
  '/',
  validate(initiateSchema),
  wrap(async (req, res) => {
    const call = await service.createCall(req.user.id, req.body);
    res.status(201).json({ call });
  })
);

router.post(
  '/:id/end',
  validate(endSchema),
  wrap(async (req, res) => {
    const call = await service.endCall(req.params.id);
    res.json({ call });
  })
);

router.get(
  '/',
  wrap(async (req, res) => {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const offset = parseInt(req.query.offset || '0', 10);
    res.json({ calls: await service.history(req.user.id, { limit, offset }) });
  })
);

router.get(
  '/:id',
  wrap(async (req, res) => {
    const call = await service.getCall(req.params.id, req.user.id);
    if (!call) return res.status(404).json({ error: 'Call not found' });
    res.json({ call });
  })
);

module.exports = router;
