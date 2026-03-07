'use strict';

const express = require('express');

function setSecurityHeaders(setter) {
  setter('Content-Security-Policy', "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'");
  setter('X-Frame-Options', 'DENY');
  setter('Referrer-Policy', 'no-referrer');
  setter('X-Content-Type-Options', 'nosniff');
  setter('Cross-Origin-Opener-Policy', 'same-origin');
  setter('Cross-Origin-Embedder-Policy', 'require-corp');
  if (process.env.FORTRESS_HSTS === 'true') {
    setter('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  }
}

function expressMiddleware(req, res, next) {
  setSecurityHeaders((name, value) => res.setHeader(name, value));
  next();
}

async function koaMiddleware(ctx, next) {
  setSecurityHeaders((name, value) => ctx.set(name, value));
  await next();
}

const router = express.Router();

router.get('/status/fo', (req, res) => {
  res.json({ status: 'ok', fortress: true });
});

module.exports = {
  expressMiddleware,
  koaMiddleware,
  router,
};
