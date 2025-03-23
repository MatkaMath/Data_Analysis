from data_fetch import load_data_from_json
from data_preprocessing import preprocess_data
from database_insert import insert_stock_data
from pathlib import Path


def main():
    #print("Loading data from JSON...")
    json_path = Path(__file__).resolve().parent.parent / 'data' / 'AAPL_data.json'
    data = load_data_from_json(json_path)

    if data is None:
        print("Failed to load data. Exiting.")
        return

    #print(f"Total records in JSON: {len(data['Time Series (5min)'])}")

    #print("Processing data...")
    data_df = preprocess_data(data)

    #print("First few rows of the processed data:")
    #print(data_df[['open', 'high', 'low', 'close', 'volume', 'sma_50', 'ema_20', 'z_score', 'anomaly']].head())

    #print("Inserting data into MySQL...")
    insert_stock_data('AAPL', data_df)


if __name__ == "__main__":
    main()
    print("✅ Data successfully processed and stored.")
