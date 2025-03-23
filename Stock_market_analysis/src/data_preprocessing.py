import pandas as pd

def preprocess_data(data):
    try:
        # Convert the JSON data to DataFrame
        data_df = pd.DataFrame.from_dict(data['Time Series (5min)'], orient='index')
    except KeyError:
        print("Error: Data format is incorrect or missing key 'Time Series (5min)'")
        return None

    data_df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    }, inplace=True)

    # Convert the index (timestamps) to datetime
    data_df.index = pd.to_datetime(data_df.index, errors='coerce')

    # Remove rows with NaN values
    data_df = data_df.dropna()

    data_df['close'] = data_df['close'].astype(float)

    # Calculate indicators
    data_df['sma_50'] = data_df['close'].rolling(window=50).mean()
    data_df['ema_20'] = data_df['close'].ewm(span=20, adjust=False).mean()
    data_df['z_score'] = (data_df['close'] - data_df['close'].mean()) / data_df['close'].std()

    # Mark anomalies
    data_df['anomaly'] = data_df['z_score'].abs() > 2
    data_df['anomaly'] = data_df['anomaly'].apply(lambda x: 'outlier' if x else 'normal')

    return data_df