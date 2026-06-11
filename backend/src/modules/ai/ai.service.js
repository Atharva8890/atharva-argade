'use strict';

const config = require('../../config');
const logger = require('../../utils/logger');

const sttOpenai = require('./providers/stt.openai');
const sttDeepgram = require('./providers/stt.deepgram');

const translateOpenai = require('./providers/translate.openai');
const translateGoogle = require('./providers/translate.google');
const translateDeepl = require('./providers/translate.deepl');
const translateAzure = require('./providers/translate.azure');

const ttsElevenlabs = require('./providers/tts.elevenlabs');
const ttsAzure = require('./providers/tts.azure');
const ttsGoogle = require('./providers/tts.google');

const STT = {
  openai: sttOpenai,
  deepgram: sttDeepgram,
};

const TRANSLATE = {
  openai: translateOpenai,
  google: translateGoogle,
  deepl: translateDeepl,
  azure: translateAzure,
};

const TTS = {
  elevenlabs: ttsElevenlabs,
  azure: ttsAzure,
  google: ttsGoogle,
};

const pick = (registry, requested, fallback) => {
  const name = (requested || '').toLowerCase();
  if (name && registry[name]) return { name, provider: registry[name] };
  logger.warn({ requested }, `Provider not found, falling back to ${fallback}`);
  return { name: fallback, provider: registry[fallback] };
};

const transcribe = async ({ audio, language, mimeType, provider }) => {
  const { name, provider: impl } = pick(STT, provider || config.ai.sttProvider, 'openai');
  const start = Date.now();
  const result = await impl.transcribe({ audio, language, mimeType });
  return { ...result, provider: name, latencyMs: Date.now() - start };
};

const translate = async ({ text, source, target, provider, context }) => {
  if (!text || !text.trim()) return { text: '', provider: 'noop', latencyMs: 0 };
  if (source === target) return { text, provider: 'noop', latencyMs: 0 };
  const { name, provider: impl } = pick(TRANSLATE, provider || config.ai.translateProvider, 'openai');
  const start = Date.now();
  const translated = await impl.translate({ text, source, target, context });
  return { text: translated, provider: name, latencyMs: Date.now() - start };
};

const synthesize = async ({ text, language, voice, provider }) => {
  if (!text) return { audio: null, provider: 'noop', latencyMs: 0 };
  const { name, provider: impl } = pick(TTS, provider || config.ai.ttsProvider, 'elevenlabs');
  const start = Date.now();
  const audio = await impl.synthesize({ text, language, voice });
  return { audio, provider: name, latencyMs: Date.now() - start };
};

const pipeline = async ({ audio, mimeType, sourceLanguage, targetLanguage, voice }) => {
  const stt = await transcribe({ audio, language: sourceLanguage, mimeType });
  const tr = await translate({ text: stt.text, source: stt.language || sourceLanguage, target: targetLanguage });
  const tts = await synthesize({ text: tr.text, language: targetLanguage, voice });
  return {
    originalText: stt.text,
    translatedText: tr.text,
    audio: tts.audio,
    providers: { stt: stt.provider, translate: tr.provider, tts: tts.provider },
    latency: {
      sttMs: stt.latencyMs,
      translateMs: tr.latencyMs,
      ttsMs: tts.latencyMs,
      totalMs: stt.latencyMs + tr.latencyMs + tts.latencyMs,
    },
  };
};

module.exports = { transcribe, translate, synthesize, pipeline };
