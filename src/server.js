'use strict';

const express = require('express');
const { expressMiddleware, router: fortressRouter } = require('./middleware/fortress');

const app = express();

// Apply Fortress security headers to all responses
app.use(expressMiddleware);

// Mount Fortress routes (e.g. GET /status/fo)
app.use(fortressRouter);

// Health check
app.get('/health', (req, res) => {
  res.json({ ok: true, service: 'joi-ai' });
});

// Only start listening when run directly (not when required by tests)
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Joi server running on port ${PORT}`);
  });
}

module.exports = app;
