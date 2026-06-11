'use strict';

const { Router } = require('express');
const multer = require('multer');
const Joi = require('joi');
const service = require('./ai.service');
const { requireAuth } = require('../../middleware/auth');
const { validate } = require('../../middleware/validate');

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 25 * 1024 * 1024 },
});

const router = Router();
router.use(requireAuth);

const translateSchema = Joi.object({
  text: Joi.string().min(1).max(5000).required(),
  source: Joi.string().lowercase().length(2).required(),
  target: Joi.string().lowercase().length(2).required(),
  provider: Joi.string().valid('openai', 'google', 'deepl', 'azure').optional(),
});

const synthesizeSchema = Joi.object({
  text: Joi.string().min(1).max(5000).required(),
  language: Joi.string().lowercase().length(2).required(),
  voice: Joi.string().max(120).optional(),
  provider: Joi.string().valid('elevenlabs', 'azure', 'google').optional(),
});

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.post(
  '/transcribe',
  upload.single('audio'),
  wrap(async (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'audio file is required' });
    const result = await service.transcribe({
      audio: req.file.buffer,
      mimeType: req.file.mimetype,
      language: req.body.language,
      provider: req.body.provider,
    });
    res.json(result);
  })
);

router.post(
  '/translate',
  validate(translateSchema),
  wrap(async (req, res) => res.json(await service.translate(req.body)))
);

router.post(
  '/tts',
  validate(synthesizeSchema),
  wrap(async (req, res) => res.json(await service.synthesize(req.body)))
);

router.post(
  '/pipeline',
  upload.single('audio'),
  wrap(async (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'audio file is required' });
    const result = await service.pipeline({
      audio: req.file.buffer,
      mimeType: req.file.mimetype,
      sourceLanguage: req.body.sourceLanguage,
      targetLanguage: req.body.targetLanguage,
      voice: req.body.voice,
    });
    res.json(result);
  })
);

module.exports = router;
