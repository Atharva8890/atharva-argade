'use strict';

const axios = require('axios');
const config = require('../../../config');

const translate = async ({ text, source, target }) => {
  if (!config.ai.googleTranslateKey) return `[GOOGLE_TRANSLATE_KEY missing] ${text}`;
  const { data } = await axios.post(
    `https://translation.googleapis.com/language/translate/v2?key=${config.ai.googleTranslateKey}`,
    { q: text, source, target, format: 'text' },
    { timeout: 15_000 }
  );
  return data?.data?.translations?.[0]?.translatedText || '';
};

module.exports = { translate };
