'use strict';

jest.mock('../src/config/db', () => ({
  pool: { on: jest.fn() },
  query: jest.fn(),
  tx: jest.fn(),
  close: jest.fn(),
}));

jest.mock('../src/config/redis', () => ({
  on: jest.fn(),
  set: jest.fn(),
  get: jest.fn(),
  del: jest.fn(),
}));

describe('Express app build', () => {
  test('builds without throwing and registers /health', async () => {
    process.env.JWT_SECRET = process.env.JWT_SECRET || 'ci-secret';
    process.env.JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'ci-refresh';
    const buildApp = require('../src/app');
    const app = buildApp();
    expect(typeof app.use).toBe('function');

    const request = require('supertest');
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('returns plan catalog without auth', async () => {
    const buildApp = require('../src/app');
    const app = buildApp();
    const request = require('supertest');
    const res = await request(app).get('/api/v1/subscriptions/plans');
    expect(res.status).toBe(200);
    expect(res.body.plans.length).toBeGreaterThan(0);
    expect(res.body.plans.find((p) => p.code === 'premium').priceInr).toBe(299);
  });

  test('returns 30+ supported languages', async () => {
    const buildApp = require('../src/app');
    const app = buildApp();
    const request = require('supertest');
    const res = await request(app).get('/api/v1/translations/languages');
    expect(res.status).toBe(200);
    expect(res.body.languages.length).toBeGreaterThanOrEqual(20);
  });

  test('rejects unauthenticated access to /me', async () => {
    const buildApp = require('../src/app');
    const app = buildApp();
    const request = require('supertest');
    const res = await request(app).get('/api/v1/auth/me');
    expect(res.status).toBe(401);
  });
});
