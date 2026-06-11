'use strict';

const axios = require('axios');
const config = require('../../../config');

const DEFAULT_VOICE = '21m00Tcm4TlvDq8ikWAM';

const synthesize = async ({ text, voice }) => {
  if (!config.ai.elevenlabsKey) return null;
  const voiceId = voice || DEFAULT_VOICE;
  const { data } = await axios.post(
    `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
    {
      text,
      model_id: 'eleven_multilingual_v2',
      voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.0, use_speaker_boost: true },
    },
    {
      headers: {
        'xi-api-key': config.ai.elevenlabsKey,
        'Content-Type': 'application/json',
        Accept: 'audio/mpeg',
      },
      responseType: 'arraybuffer',
      timeout: 30_000,
    }
  );
  return { mimeType: 'audio/mpeg', data: Buffer.from(data).toString('base64') };
};

module.exports = { synthesize };
