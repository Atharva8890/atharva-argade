'use strict';

const axios = require('axios');
const FormData = require('form-data');
const config = require('../../../config');

const transcribe = async ({ audio, language, mimeType = 'audio/webm' }) => {
  if (!config.ai.openaiKey) {
    return { text: '[OPENAI_API_KEY missing - stub transcription]', language };
  }
  const buffer = Buffer.isBuffer(audio) ? audio : Buffer.from(audio);
  const form = new FormData();
  form.append('file', buffer, { filename: 'audio.webm', contentType: mimeType });
  form.append('model', 'whisper-1');
  if (language) form.append('language', language);
  form.append('response_format', 'json');

  const { data } = await axios.post('https://api.openai.com/v1/audio/transcriptions', form, {
    headers: {
      ...form.getHeaders(),
      Authorization: `Bearer ${config.ai.openaiKey}`,
    },
    maxBodyLength: 50 * 1024 * 1024,
    timeout: 30_000,
  });
  return { text: data.text, language: data.language || language };
};

module.exports = { transcribe };
