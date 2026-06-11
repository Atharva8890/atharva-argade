'use strict';

const { Router } = require('express');
const Joi = require('joi');
const service = require('./users.service');
const { validate } = require('../../middleware/validate');
const { requireAuth } = require('../../middleware/auth');

const router = Router();
router.use(requireAuth);

const updateSchema = Joi.object({
  name: Joi.string().min(2).max(80),
  phone: Joi.string().pattern(/^\+?[0-9]{8,15}$/),
  language: Joi.string().lowercase().length(2),
  avatar_url: Joi.string().uri(),
}).min(1);

const addContactSchema = Joi.object({
  email: Joi.string().email().required(),
  alias: Joi.string().max(80).optional(),
});

const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

router.patch(
  '/me',
  validate(updateSchema),
  wrap(async (req, res) => {
    const user = await service.updateProfile(req.user.id, req.body);
    res.json({ user });
  })
);

router.delete(
  '/me',
  wrap(async (req, res) => {
    await service.deleteAccount(req.user.id);
    res.status(204).end();
  })
);

router.get(
  '/contacts',
  wrap(async (req, res) => {
    res.json({ contacts: await service.listContacts(req.user.id) });
  })
);

router.post(
  '/contacts',
  validate(addContactSchema),
  wrap(async (req, res) => {
    res.status(201).json({ contact: await service.addContact(req.user.id, req.body) });
  })
);

router.delete(
  '/contacts/:contactUserId',
  wrap(async (req, res) => {
    await service.removeContact(req.user.id, req.params.contactUserId);
    res.status(204).end();
  })
);

module.exports = router;
