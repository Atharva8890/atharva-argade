'use strict';

const axios = require('axios');
const config = require('../../../config');
const { nameOf } = require('../../../utils/languages');

const translate = async ({ text, source, target, context }) => {
  if (!config.ai.openaiKey) {
    return `[OPENAI_API_KEY missing] ${text}`;
  }
  const system = `You are a professional real-time interpreter. Translate the user's message from ${nameOf(source)} to ${nameOf(target)}.
- Preserve meaning, tone, register, and named entities.
- Do not add explanations or quotation marks.
- Output only the translated sentence.
${context ? `\nConversation context (for terminology consistency):\n${context}` : ''}`;

  const { data } = await axios.post(
    'https://api.openai.com/v1/chat/completions',
    {
      model: 'gpt-4o-mini',
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: text },
      ],
    },
    {
      headers: {
        Authorization: `Bearer ${config.ai.openaiKey}`,
        'Content-Type': 'application/json',
      },
      timeout: 20_000,
    }
  );
  return data?.choices?.[0]?.message?.content?.trim() || '';
};

module.exports = { translate };
