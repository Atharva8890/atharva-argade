'use strict';

const http = require('http');
const buildApp = require('./app');
const config = require('./config');
const logger = require('./utils/logger');
const { init: initSocket } = require('./realtime/socket');
const db = require('./config/db');

const main = async () => {
  const app = buildApp();
  const server = http.createServer(app);
  initSocket(server);

  server.listen(config.port, () => {
    logger.info(`VoiceBridge AI backend listening on :${config.port} (${config.env})`);
  });

  const shutdown = async (signal) => {
    logger.info({ signal }, 'Shutting down');
    server.close(() => logger.info('HTTP server closed'));
    try {
      await db.close();
    } catch (err) {
      logger.error({ err }, 'Error closing DB');
    }
    setTimeout(() => process.exit(0), 1000).unref();
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('unhandledRejection', (err) => logger.error({ err }, 'unhandledRejection'));
  process.on('uncaughtException', (err) => {
    logger.error({ err }, 'uncaughtException');
    setTimeout(() => process.exit(1), 100).unref();
  });
};

main().catch((err) => {
  logger.error({ err }, 'Fatal startup error');
  process.exit(1);
});
