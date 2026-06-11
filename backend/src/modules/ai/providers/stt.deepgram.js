'use strict';

const axios = require('axios');
const config = require('../../../config');

const transcribe = async ({ audio, language, mimeType = 'audio/webm' }) => {
  if (!config.ai.deepgramKey) {
    return { text: '[DEEPGRAM_API_KEY missing - stub transcription]', language };
  }
  const params = new URLSearchParams({
    model: 'nova-2-general',
    smart_format: 'true',
    punctuate: 'true',
    ...(language ? { language } : { detect_language: 'true' }),
  });

  const { data } = await axios.post(
    `https://api.deepgram.com/v1/listen?${params.toString()}`,
    Buffer.isBuffer(audio) ? audio : Buffer.from(audio),
    {
      headers: {
        Authorization: `Token ${config.ai.deepgramKey}`,
        'Content-Type': mimeType,
      },
      timeout: 30_000,
      maxBodyLength: 50 * 1024 * 1024,
    }
  );
  const alt = data?.results?.channels?.[0]?.alternatives?.[0];
  return {
    text: alt?.transcript || '',
    language: data?.results?.channels?.[0]?.detected_language || language,
  };
};

module.exports = { transcribe };
