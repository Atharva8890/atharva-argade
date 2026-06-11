'use strict';

const axios = require('axios');
const config = require('../../../config');

const synthesize = async ({ text, language }) => {
  if (!config.ai.googleTtsKey) return null;
  const { data } = await axios.post(
    `https://texttospeech.googleapis.com/v1/text:synthesize?key=${config.ai.googleTtsKey}`,
    {
      input: { text },
      voice: { languageCode: language || 'en-US', ssmlGender: 'FEMALE' },
      audioConfig: { audioEncoding: 'MP3' },
    },
    { timeout: 30_000 }
  );
  return data?.audioContent ? { mimeType: 'audio/mpeg', data: data.audioContent } : null;
};

module.exports = { synthesize };
