'use strict';

const axios = require('axios');
const config = require('../../../config');

const translate = async ({ text, source, target }) => {
  if (!config.ai.deeplKey) return `[DEEPL_API_KEY missing] ${text}`;
  const params = new URLSearchParams();
  params.append('text', text);
  params.append('target_lang', String(target).toUpperCase());
  if (source) params.append('source_lang', String(source).toUpperCase());

  const { data } = await axios.post('https://api-free.deepl.com/v2/translate', params, {
    headers: {
      Authorization: `DeepL-Auth-Key ${config.ai.deeplKey}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    timeout: 15_000,
  });
  return data?.translations?.[0]?.text || '';
};

module.exports = { translate };
