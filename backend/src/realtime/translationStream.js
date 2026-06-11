'use strict';

const logger = require('../utils/logger');
const ai = require('../modules/ai/ai.service');
const translations = require('../modules/translations/translations.service');

/**
 * Live translation socket protocol
 * -------------------------------------------------------------------------
 * Client sends audio chunks (Buffer / base64) as they speak. We run the
 * STT → translate → TTS pipeline per chunk and broadcast results to peers
 * in the same call room.
 *
 * Inbound events:
 *   translate:chunk { callId, chunk (base64 or Buffer), mimeType, sourceLanguage, targets: [{ userId, language, voice? }] }
 *   translate:text  { callId, text, sourceLanguage, targets: [...] }
 *
 * Outbound events (per peer):
 *   caption:original   { callId, speakerId, text, language, ts }
 *   caption:translated { callId, speakerId, text, language, ts }
 *   audio:translated   { callId, speakerId, audio, mimeType, language }
 */
const register = (io, socket) => {
  socket.on('translate:chunk', async (payload, ack) => {
    const { callId, chunk, mimeType = 'audio/webm', sourceLanguage, targets = [] } = payload;
    if (!callId || !chunk || !sourceLanguage) {
      return ack?.({ ok: false, error: 'callId, chunk, sourceLanguage are required' });
    }
    try {
      const buf = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, 'base64');
      const stt = await ai.transcribe({ audio: buf, mimeType, language: sourceLanguage });
      if (!stt.text || !stt.text.trim()) return ack?.({ ok: true, empty: true });

      io.to(`call:${callId}`).emit('caption:original', {
        callId,
        speakerId: socket.user.id,
        text: stt.text,
        language: stt.language || sourceLanguage,
        ts: Date.now(),
      });

      await Promise.all(
        targets.map(async (t) => {
          try {
            const tr = await ai.translate({ text: stt.text, source: sourceLanguage, target: t.language });
            const tts = await ai.synthesize({ text: tr.text, language: t.language, voice: t.voice });
            io.to(`user:${t.userId}`).emit('caption:translated', {
              callId,
              speakerId: socket.user.id,
              text: tr.text,
              language: t.language,
              ts: Date.now(),
            });
            if (tts.audio) {
              io.to(`user:${t.userId}`).emit('audio:translated', {
                callId,
                speakerId: socket.user.id,
                audio: tts.audio.data,
                mimeType: tts.audio.mimeType,
                language: t.language,
              });
            }
            await translations.log({
              callId,
              speakerId: socket.user.id,
              sourceLanguage,
              targetLanguage: t.language,
              originalText: stt.text,
              translatedText: tr.text,
              provider: `${stt.provider}+${tr.provider}+${tts.provider}`,
              latencyMs: stt.latencyMs + tr.latencyMs + tts.latencyMs,
            });
          } catch (err) {
            logger.error({ err: err.message, userId: t.userId }, 'translation fan-out failed');
          }
        })
      );

      ack?.({ ok: true });
    } catch (err) {
      logger.error({ err }, 'translate:chunk failed');
      ack?.({ ok: false, error: err.message });
    }
  });

  socket.on('translate:text', async (payload, ack) => {
    const { callId, text, sourceLanguage, targets = [] } = payload;
    try {
      io.to(`call:${callId}`).emit('caption:original', {
        callId,
        speakerId: socket.user.id,
        text,
        language: sourceLanguage,
        ts: Date.now(),
      });
      await Promise.all(
        targets.map(async (t) => {
          const tr = await ai.translate({ text, source: sourceLanguage, target: t.language });
          io.to(`user:${t.userId}`).emit('caption:translated', {
            callId,
            speakerId: socket.user.id,
            text: tr.text,
            language: t.language,
            ts: Date.now(),
          });
          await translations.log({
            callId,
            speakerId: socket.user.id,
            sourceLanguage,
            targetLanguage: t.language,
            originalText: text,
            translatedText: tr.text,
            provider: tr.provider,
            latencyMs: tr.latencyMs,
          });
        })
      );
      ack?.({ ok: true });
    } catch (err) {
      logger.error({ err }, 'translate:text failed');
      ack?.({ ok: false, error: err.message });
    }
  });
};

module.exports = { register };
