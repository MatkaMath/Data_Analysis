import config
import mysql.connector
from mysql.connector import Error
import math

def insert_stock_data(symbol, data_df):
    conn = mysql.connector.connect(
        host=config.DATABASE['host'],
        user=config.DATABASE['user'],
        password=config.DATABASE['password'],
        database=config.DATABASE['database']
    )
    cursor = conn.cursor()

    query = """
    INSERT INTO stock_data 
    (symbol, timestamp, open, high, low, close, volume, sma_50, ema_20, z_score, anomaly)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      open = VALUES(open),
      high = VALUES(high),
      low = VALUES(low),
      close = VALUES(close),
      volume = VALUES(volume),
      sma_50 = VALUES(sma_50),
      ema_20 = VALUES(ema_20),
      z_score = VALUES(z_score),
      anomaly = VALUES(anomaly);
    """

    for index, row in data_df.iterrows():
        try:
            cursor.execute(query, (
                symbol,
                index,
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['volume']),
                None if math.isnan(row.get('sma_50', float('nan'))) else float(row['sma_50']),
                None if math.isnan(row.get('ema_20', float('nan'))) else float(row['ema_20']),
                None if math.isnan(row.get('z_score', float('nan'))) else float(row['z_score']),
                row.get('anomaly', None)
            ))
        except Exception as e:
            print(f"Error inserting row: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
