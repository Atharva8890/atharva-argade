'use strict';

const logger = require('../utils/logger');
const callsService = require('../modules/calls/calls.service');
const config = require('../config');

const register = (io, socket) => {
  socket.on('call:invite', async (payload, ack) => {
    try {
      const { callId, peerIds = [] } = payload;
      peerIds.forEach((peerId) => {
        io.to(`user:${peerId}`).emit('call:incoming', {
          callId,
          from: socket.user,
          startedAt: Date.now(),
        });
      });
      ack?.({ ok: true });
    } catch (err) {
      logger.error({ err }, 'call:invite failed');
      ack?.({ ok: false, error: err.message });
    }
  });

  socket.on('call:join', async ({ callId }, ack) => {
    if (!callId) return ack?.({ ok: false, error: 'callId required' });
    socket.join(`call:${callId}`);
    socket.to(`call:${callId}`).emit('peer:joined', { userId: socket.user.id });
    ack?.({ ok: true, iceServers: config.webrtc.iceServers });
  });

  socket.on('call:leave', async ({ callId }, ack) => {
    socket.leave(`call:${callId}`);
    socket.to(`call:${callId}`).emit('peer:left', { userId: socket.user.id });
    ack?.({ ok: true });
  });

  socket.on('call:end', async ({ callId }, ack) => {
    try {
      const call = await callsService.endCall(callId);
      io.to(`call:${callId}`).emit('call:ended', { callId, durationSec: call?.duration_sec });
      ack?.({ ok: true, call });
    } catch (err) {
      ack?.({ ok: false, error: err.message });
    }
  });

  socket.on('webrtc:offer', ({ callId, to, sdp }) => {
    io.to(`user:${to}`).emit('webrtc:offer', { callId, from: socket.user.id, sdp });
  });

  socket.on('webrtc:answer', ({ callId, to, sdp }) => {
    io.to(`user:${to}`).emit('webrtc:answer', { callId, from: socket.user.id, sdp });
  });

  socket.on('webrtc:ice', ({ callId, to, candidate }) => {
    io.to(`user:${to}`).emit('webrtc:ice', { callId, from: socket.user.id, candidate });
  });

  socket.on('call:mute', ({ callId, muted }) => {
    socket.to(`call:${callId}`).emit('peer:muted', { userId: socket.user.id, muted });
  });
};

module.exports = { register };
