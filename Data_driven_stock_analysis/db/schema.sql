CREATE DATABASE stockdb;
USE stockdb;

-- Symbols master
CREATE TABLE IF NOT EXISTS symbols (
  symbol        VARCHAR(32) PRIMARY KEY,
  company       VARCHAR(128) NOT NULL,
  sector        VARCHAR(64)  NOT NULL
);

-- Daily prices (1 row per symbol-date)
CREATE TABLE IF NOT EXISTS prices (
  trade_date    DATE NOT NULL,
  symbol        VARCHAR(32) NOT NULL,
  open_price    DECIMAL(12,4),
  high_price    DECIMAL(12,4),
  low_price     DECIMAL(12,4),
  close_price   DECIMAL(12,4),
  volume        BIGINT,
  PRIMARY KEY (trade_date, symbol),
  FOREIGN KEY (symbol) REFERENCES symbols(symbol)
);

-- Helpful indexes
CREATE INDEX idx_prices_symbol ON prices(symbol);
CREATE INDEX idx_prices_date   ON prices(trade_date);

USE stockdb;

-- Temporarily disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing dependent tables
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS symbols;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

USE stockdb;

-- 1️⃣ Confirm both tables exist
SHOW TABLES;

-- 2️⃣ Check number of rows in each
SELECT COUNT(*) AS total_symbols FROM symbols;
SELECT COUNT(*) AS total_prices FROM prices;

-- 3️⃣ View first few records
SELECT * FROM symbols LIMIT 5;
SELECT * FROM prices LIMIT 5;

-- 4️⃣ Verify foreign-key linkage (optional)
SELECT COUNT(DISTINCT symbol) AS unique_symbols_in_prices FROM prices;
