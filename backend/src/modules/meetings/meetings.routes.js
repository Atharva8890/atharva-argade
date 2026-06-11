'use strict';

const { Router } = require('express');
const Joi = require('joi');
const service = require('./meetings.service');
const { requireAuth } = require('../../middleware/auth');
const { validate } = require('../../middleware/validate');

const router = Router();
router.use(requireAuth);

const createSchema = Joi.object({
  title: Joi.string().min(2).max(120).required(),
  scheduledAt: Joi.date().iso().optional(),
  defaultLanguage: Joi.string().lowercase().length(2).default('en'),
});

const joinSchema = Joi.object({
  meetingId: Joi.string().uuid(),
  joinCode: Joi.string().min(4).max(16),
  language: Joi.string().lowercase().length(2),
}).or('meetingId', 'joinCode');

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.post(
  '/',
  validate(createSchema),
  wrap(async (req, res) => res.status(201).json({ meeting: await service.create(req.user.id, req.body) }))
);

router.post(
  '/join',
  validate(joinSchema),
  wrap(async (req, res) => {
    const meeting = await service.join(req.user.id, req.body);
    if (!meeting) return res.status(404).json({ error: 'Meeting not found' });
    res.json({ meeting });
  })
);

router.get(
  '/:id/transcript',
  wrap(async (req, res) => res.json({ segments: await service.transcript(req.params.id) }))
);

router.post(
  '/:id/summary',
  wrap(async (req, res) => res.json(await service.generateSummary(req.params.id)))
);

module.exports = router;
