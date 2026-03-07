'use strict';

const request = require('supertest');
const app = require('../src/server');

describe('Fortress Middleware', () => {
  it('GET /health returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.ok).toBe(true);
  });

  it('GET /status/fo returns fortress status', async () => {
    const res = await request(app).get('/status/fo');
    expect(res.status).toBe(200);
    expect(res.body.fortress).toBe(true);
    expect(res.body.status).toBe('ok');
  });

  it('sets Content-Security-Policy header', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['content-security-policy']).toBeDefined();
    expect(res.headers['content-security-policy']).toContain("default-src 'self'");
  });

  it('sets X-Frame-Options: DENY', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['x-frame-options']).toBe('DENY');
  });

  it('sets X-Content-Type-Options: nosniff', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['x-content-type-options']).toBe('nosniff');
  });

  it('sets Referrer-Policy: no-referrer', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['referrer-policy']).toBe('no-referrer');
  });

  it('sets Cross-Origin-Opener-Policy: same-origin', async () => {
    const res = await request(app).get('/health');
    expect(res.headers['cross-origin-opener-policy']).toBe('same-origin');
  });
});
