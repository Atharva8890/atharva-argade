'use strict';

const axios = require('axios');
const config = require('../../../config');

const translate = async ({ text, source, target }) => {
  if (!config.ai.azureTranslatorKey) return `[AZURE_TRANSLATOR_KEY missing] ${text}`;
  const params = new URLSearchParams({ 'api-version': '3.0', to: target });
  if (source) params.append('from', source);
  const { data } = await axios.post(
    `https://api.cognitive.microsofttranslator.com/translate?${params.toString()}`,
    [{ Text: text }],
    {
      headers: {
        'Ocp-Apim-Subscription-Key': config.ai.azureTranslatorKey,
        'Ocp-Apim-Subscription-Region': config.ai.azureTranslatorRegion,
        'Content-Type': 'application/json',
      },
      timeout: 15_000,
    }
  );
  return data?.[0]?.translations?.[0]?.text || '';
};

module.exports = { translate };
