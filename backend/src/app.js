'use strict';

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');

const config = require('./config');
const logger = require('./utils/logger');
const { notFound, errorHandler } = require('./middleware/error');
const { apiLimiter } = require('./middleware/rateLimit');

const authRoutes = require('./modules/auth/auth.routes');
const userRoutes = require('./modules/users/users.routes');
const callRoutes = require('./modules/calls/calls.routes');
const translationRoutes = require('./modules/translations/translations.routes');
const aiRoutes = require('./modules/ai/ai.routes');
const chatRoutes = require('./modules/chat/chat.routes');
const meetingRoutes = require('./modules/meetings/meetings.routes');
const subscriptionRoutes = require('./modules/subscriptions/subscriptions.routes');

const buildApp = () => {
  const app = express();

  app.set('trust proxy', 1);

  app.use(helmet({ crossOriginResourcePolicy: false }));
  app.use(
    cors({
      origin: config.cors.origins.includes('*') ? true : config.cors.origins,
      credentials: true,
    })
  );
  app.use(compression());
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));
  app.use(cookieParser());
  app.use(
    morgan('tiny', {
      stream: { write: (m) => logger.info(m.trim()) },
      skip: (req) => req.path === '/health',
    })
  );

  app.get('/', (_req, res) => res.json({ name: 'VoiceBridge AI API', version: '0.1.0', status: 'ok' }));
  app.get('/health', (_req, res) => res.json({ status: 'ok', ts: new Date().toISOString() }));

  app.use('/api/v1', apiLimiter);
  app.use('/api/v1/auth', authRoutes);
  app.use('/api/v1/users', userRoutes);
  app.use('/api/v1/calls', callRoutes);
  app.use('/api/v1/translations', translationRoutes);
  app.use('/api/v1/ai', aiRoutes);
  app.use('/api/v1/chat', chatRoutes);
  app.use('/api/v1/meetings', meetingRoutes);
  app.use('/api/v1/subscriptions', subscriptionRoutes);

  app.use(notFound);
  app.use(errorHandler);

  return app;
};

module.exports = buildApp;
