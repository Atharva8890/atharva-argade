'use strict';

const { Server } = require('socket.io');
const { verifyAccess } = require('../utils/jwt');
const logger = require('../utils/logger');
const config = require('../config');
const signaling = require('./signaling');
const translationStream = require('./translationStream');

const attachAuth = (socket, next) => {
  const token = socket.handshake.auth?.token || socket.handshake.headers?.authorization?.replace(/^Bearer\s+/i, '');
  if (!token) return next(new Error('Authentication required'));
  try {
    const payload = verifyAccess(token);
    socket.user = { id: payload.sub, email: payload.email, plan: payload.plan };
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
};

const init = (httpServer) => {
  const io = new Server(httpServer, {
    cors: {
      origin: config.cors.origins.includes('*') ? true : config.cors.origins,
      credentials: true,
    },
    maxHttpBufferSize: 20 * 1024 * 1024,
    pingInterval: 20_000,
    pingTimeout: 25_000,
  });

  io.use(attachAuth);

  io.on('connection', (socket) => {
    logger.info({ userId: socket.user.id, sid: socket.id }, 'socket connected');

    socket.join(`user:${socket.user.id}`);

    signaling.register(io, socket);
    translationStream.register(io, socket);

    socket.on('disconnect', (reason) => {
      logger.info({ userId: socket.user.id, sid: socket.id, reason }, 'socket disconnected');
    });
  });

  return io;
};

module.exports = { init };
