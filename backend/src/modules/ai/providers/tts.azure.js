'use strict';

const axios = require('axios');
const config = require('../../../config');

const voiceFor = (lang) => {
  const map = {
    en: 'en-US-JennyNeural',
    hi: 'hi-IN-SwaraNeural',
    mr: 'mr-IN-AarohiNeural',
    gu: 'gu-IN-DhwaniNeural',
    pa: 'pa-IN-OjasNeural',
    ta: 'ta-IN-PallaviNeural',
    te: 'te-IN-ShrutiNeural',
    kn: 'kn-IN-SapnaNeural',
    ml: 'ml-IN-SobhanaNeural',
    bn: 'bn-IN-TanishaaNeural',
    ur: 'ur-IN-GulNeural',
    ar: 'ar-EG-SalmaNeural',
    zh: 'zh-CN-XiaoxiaoNeural',
    ja: 'ja-JP-NanamiNeural',
    ko: 'ko-KR-SunHiNeural',
    fr: 'fr-FR-DeniseNeural',
    de: 'de-DE-KatjaNeural',
    es: 'es-ES-ElviraNeural',
    ru: 'ru-RU-SvetlanaNeural',
  };
  return map[lang] || 'en-US-JennyNeural';
};

const synthesize = async ({ text, language, voice }) => {
  if (!config.ai.azureTtsKey || !config.ai.azureTtsRegion) return null;
  const voiceName = voice || voiceFor(language);
  const ssml = `<speak version='1.0' xml:lang='${voiceName.slice(0, 5)}'>
    <voice name='${voiceName}'>${text.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</voice>
  </speak>`;

  const { data } = await axios.post(
    `https://${config.ai.azureTtsRegion}.tts.speech.microsoft.com/cognitiveservices/v1`,
    ssml,
    {
      headers: {
        'Ocp-Apim-Subscription-Key': config.ai.azureTtsKey,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
        'User-Agent': 'voicebridge-ai',
      },
      responseType: 'arraybuffer',
      timeout: 30_000,
    }
  );
  return { mimeType: 'audio/mpeg', data: Buffer.from(data).toString('base64') };
};

module.exports = { synthesize };
