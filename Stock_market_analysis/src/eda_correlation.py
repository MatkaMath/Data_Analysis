import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_fetch import load_data_from_json
from data_preprocessing import preprocess_data
from pathlib import Path

json_path = Path(__file__).resolve().parent.parent / 'data' / 'AAPL_data.json'
raw_data = load_data_from_json(json_path)
data_df = preprocess_data(raw_data)
data_df = data_df.sort_index()

data_df['open'] = data_df['open'].astype(float)
data_df['high'] = data_df['high'].astype(float)
data_df['low'] = data_df['low'].astype(float)
data_df['close'] = data_df['close'].astype(float)
data_df['volume'] = data_df['volume'].astype(int)

data_df['volatility'] = data_df['high'] - data_df['low']

cols_for_corr = ['open', 'high', 'low', 'close', 'volume', 'sma_50', 'ema_20', 'z_score', 'volatility']
corr_df = data_df[cols_for_corr].dropna()

correlation_matrix = corr_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Matrix of Stock Features")
plt.tight_layout()
plt.show()
