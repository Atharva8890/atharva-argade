'use strict';

require('dotenv').config();

const required = (name, fallback) => {
  const value = process.env[name] ?? fallback;
  if (value === undefined || value === '') {
    if (process.env.NODE_ENV === 'production') {
      throw new Error(`Missing required environment variable: ${name}`);
    }
    return fallback;
  }
  return value;
};

const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '4000', 10),
  logLevel: process.env.LOG_LEVEL || 'info',

  databaseUrl: required(
    'DATABASE_URL',
    'postgres://voicebridge:changeme@localhost:5432/voicebridge'
  ),
  redisUrl: required('REDIS_URL', 'redis://localhost:6379'),

  cors: {
    origins: (process.env.CORS_ORIGINS || '*')
      .split(',')
      .map((o) => o.trim())
      .filter(Boolean),
  },

  jwt: {
    accessSecret: required('JWT_SECRET', 'dev-access-secret-change-me'),
    refreshSecret: required('JWT_REFRESH_SECRET', 'dev-refresh-secret-change-me'),
    accessTtl: process.env.JWT_EXPIRES_IN || '15m',
    refreshTtl: process.env.JWT_REFRESH_EXPIRES_IN || '30d',
  },

  crypto: {
    aesKey: process.env.AES_ENCRYPTION_KEY || '',
  },

  rateLimit: {
    auth: parseInt(process.env.RATE_LIMIT_AUTH || '30', 10),
    api: parseInt(process.env.RATE_LIMIT_API || '120', 10),
  },

  ai: {
    sttProvider: process.env.STT_PROVIDER || 'openai',
    translateProvider: process.env.TRANSLATE_PROVIDER || 'openai',
    ttsProvider: process.env.TTS_PROVIDER || 'elevenlabs',
    openaiKey: process.env.OPENAI_API_KEY || '',
    deepgramKey: process.env.DEEPGRAM_API_KEY || '',
    googleSpeechKey: process.env.GOOGLE_SPEECH_KEY || '',
    googleTranslateKey: process.env.GOOGLE_TRANSLATE_KEY || '',
    deeplKey: process.env.DEEPL_API_KEY || '',
    azureTranslatorKey: process.env.AZURE_TRANSLATOR_KEY || '',
    azureTranslatorRegion: process.env.AZURE_TRANSLATOR_REGION || '',
    elevenlabsKey: process.env.ELEVENLABS_API_KEY || '',
    azureTtsKey: process.env.AZURE_TTS_KEY || '',
    azureTtsRegion: process.env.AZURE_TTS_REGION || '',
    googleTtsKey: process.env.GOOGLE_TTS_KEY || '',
  },

  oauth: {
    google: {
      clientId: process.env.GOOGLE_OAUTH_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_OAUTH_CLIENT_SECRET || '',
    },
    apple: {
      clientId: process.env.APPLE_OAUTH_CLIENT_ID || '',
      teamId: process.env.APPLE_OAUTH_TEAM_ID || '',
      keyId: process.env.APPLE_OAUTH_KEY_ID || '',
      privateKey: process.env.APPLE_OAUTH_PRIVATE_KEY || '',
    },
  },

  otp: {
    twilio: {
      sid: process.env.TWILIO_ACCOUNT_SID || '',
      token: process.env.TWILIO_AUTH_TOKEN || '',
      from: process.env.TWILIO_FROM_NUMBER || '',
    },
    msg91: {
      authKey: process.env.MSG91_AUTH_KEY || '',
      templateId: process.env.MSG91_TEMPLATE_ID || '',
    },
  },

  payments: {
    razorpay: {
      keyId: process.env.RAZORPAY_KEY_ID || '',
      keySecret: process.env.RAZORPAY_KEY_SECRET || '',
      webhookSecret: process.env.RAZORPAY_WEBHOOK_SECRET || '',
    },
    stripe: {
      secretKey: process.env.STRIPE_SECRET_KEY || '',
      webhookSecret: process.env.STRIPE_WEBHOOK_SECRET || '',
      publicKey: process.env.STRIPE_PUBLIC_KEY || '',
    },
  },

  storage: {
    endpoint: process.env.S3_ENDPOINT || '',
    region: process.env.S3_REGION || 'us-east-1',
    bucket: process.env.S3_BUCKET || 'voicebridge-recordings',
    accessKey: process.env.S3_ACCESS_KEY || '',
    secretKey: process.env.S3_SECRET_KEY || '',
  },

  webrtc: {
    iceServers: [
      { urls: process.env.STUN_URL || 'stun:stun.l.google.com:19302' },
      ...(process.env.TURN_URL
        ? [
            {
              urls: process.env.TURN_URL,
              username: process.env.TURN_USERNAME || '',
              credential: process.env.TURN_PASSWORD || '',
            },
          ]
        : []),
    ],
  },
};

module.exports = config;
