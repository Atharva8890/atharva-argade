'use strict';

const { Router } = require('express');
const service = require('./translations.service');
const { requireAuth } = require('../../middleware/auth');
const { LANGUAGES } = require('../../utils/languages');

const router = Router();

router.get('/languages', (_req, res) => res.json({ languages: LANGUAGES }));

router.use(requireAuth);

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.get(
  '/calls/:callId/transcript',
  wrap(async (req, res) => {
    res.json({ transcript: await service.transcript(req.params.callId) });
  })
);

router.get(
  '/calls/:callId/summary',
  wrap(async (req, res) => {
    res.json({ summary: await service.summary(req.params.callId) });
  })
);

module.exports = router;
