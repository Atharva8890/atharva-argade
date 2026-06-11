'use strict';

describe('VoiceBridge backend smoke test', () => {
  test('config loads without throwing', () => {
    process.env.NODE_ENV = process.env.NODE_ENV || 'test';
    const config = require('../src/config');
    expect(config.port).toBeDefined();
    expect(config.jwt.accessSecret).toBeDefined();
  });

  test('languages utility covers required Indian + global languages', () => {
    const { LANGUAGES, isSupported, nameOf } = require('../src/utils/languages');
    const required = ['en', 'hi', 'mr', 'gu', 'pa', 'ta', 'te', 'kn', 'ml', 'bn', 'ur', 'ar', 'zh', 'ja', 'ko', 'fr', 'de', 'es', 'ru'];
    required.forEach((code) => expect(isSupported(code)).toBe(true));
    expect(LANGUAGES.length).toBeGreaterThanOrEqual(20);
    expect(nameOf('mr')).toBe('Marathi');
  });

  test('jwt round-trips a payload', () => {
    process.env.JWT_SECRET = process.env.JWT_SECRET || 'test-access-secret';
    process.env.JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'test-refresh-secret';
    delete require.cache[require.resolve('../src/config')];
    delete require.cache[require.resolve('../src/utils/jwt')];
    const { issueTokens, verifyAccess } = require('../src/utils/jwt');
    const tokens = issueTokens({ id: 'u1', email: 'a@b.c', subscription_plan: 'free' });
    const payload = verifyAccess(tokens.accessToken);
    expect(payload.sub).toBe('u1');
  });

  test('aes-256-gcm encrypt → decrypt round-trip', () => {
    const { encrypt, decrypt } = require('../src/utils/crypto');
    const ct = encrypt('hello voicebridge');
    expect(decrypt(ct)).toBe('hello voicebridge');
  });
});
