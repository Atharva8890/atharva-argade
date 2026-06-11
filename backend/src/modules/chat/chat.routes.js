'use strict';

const { Router } = require('express');
const Joi = require('joi');
const service = require('./chat.service');
const { requireAuth } = require('../../middleware/auth');
const { validate } = require('../../middleware/validate');

const router = Router();
router.use(requireAuth);

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

const openSchema = Joi.object({ peerId: Joi.string().uuid().required() });
const sendSchema = Joi.object({
  text: Joi.string().max(5000),
  type: Joi.string().valid('text', 'voice', 'image', 'document').default('text'),
  mediaUrl: Joi.string().uri(),
  sourceLanguage: Joi.string().lowercase().length(2),
  targetLanguage: Joi.string().lowercase().length(2),
  autoTranslate: Joi.boolean().default(true),
}).or('text', 'mediaUrl');

router.get(
  '/threads',
  wrap(async (req, res) => res.json({ threads: await service.listThreads(req.user.id) }))
);

router.post(
  '/threads',
  validate(openSchema),
  wrap(async (req, res) => {
    const thread = await service.getOrCreateThread(req.user.id, req.body.peerId);
    res.json({ thread });
  })
);

router.get(
  '/threads/:id/messages',
  wrap(async (req, res) => {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const before = req.query.before;
    res.json({ messages: await service.listMessages(req.params.id, { limit, before }) });
  })
);

router.post(
  '/threads/:id/messages',
  validate(sendSchema),
  wrap(async (req, res) => {
    const message = await service.sendMessage({
      threadId: req.params.id,
      senderId: req.user.id,
      ...req.body,
    });
    res.status(201).json({ message });
  })
);

module.exports = router;
