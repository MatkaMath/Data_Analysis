CREATE DATABASE IF NOT EXISTS stock_market;
USE stock_market;

CREATE TABLE IF NOT EXISTS stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    timestamp DATETIME,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INT,
    sma_50 FLOAT,
    ema_20 FLOAT,
    z_score FLOAT,
    anomaly VARCHAR(10),
    UNIQUE(symbol, timestamp)
);
