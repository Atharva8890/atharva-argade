#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { pool } = require('../src/config/db');
const logger = require('../src/utils/logger');

const run = async () => {
  const dir = path.join(__dirname, '..', 'migrations');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.sql')).sort();
  for (const file of files) {
    const sql = fs.readFileSync(path.join(dir, file), 'utf8');
    logger.info(`Applying ${file}`);
    await pool.query(sql);
  }
  logger.info('Migrations complete');
  await pool.end();
};

run().catch((err) => {
  logger.error({ err }, 'Migration failed');
  process.exit(1);
});
