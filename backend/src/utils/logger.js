'use strict';

const pino = require('pino');

const isDev = (process.env.NODE_ENV || 'development') !== 'production';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  base: { service: 'voicebridge-backend' },
  ...(isDev && {
    transport: {
      target: 'pino-pretty',
      options: {
        colorize: true,
        translateTime: 'SYS:standard',
        ignore: 'pid,hostname,service',
      },
    },
  }),
});

module.exports = logger;
