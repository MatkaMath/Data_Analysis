import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_fetch import load_data_from_json
from data_preprocessing import preprocess_data
from pathlib import Path

json_path = Path(__file__).resolve().parent.parent / 'data' / 'AAPL_data.json'
raw_data = load_data_from_json(json_path)

data_df = preprocess_data(raw_data)
data_df = data_df.sort_index()

data_df['close'] = data_df['close'].astype(float)
data_df['volume'] = data_df['volume'].astype(int)
data_df['high'] = data_df['high'].astype(float)
data_df['low'] = data_df['low'].astype(float)

# Calculate volatility and derived metrics
data_df['volatility'] = data_df['high'] - data_df['low']
data_df['rolling_volatility'] = data_df['volatility'].rolling(window=20).mean()
data_df['day'] = data_df.index.day_name()
data_df['hour'] = data_df.index.hour

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Volatility Analysis', fontsize=16)

# 1. Histogram of volatility
sns.histplot(data_df['volatility'], bins=40, kde=True, ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Distribution of Volatility')
axes[0, 0].set_xlabel('Volatility (High - Low)')
axes[0, 0].set_ylabel('Frequency')

# 2. Line chart with rolling average
axes[0, 1].plot(data_df.index, data_df['volatility'], label='Volatility', color='lightblue')
axes[0, 1].plot(data_df.index, data_df['rolling_volatility'], label='Rolling Avg (20)', color='orange')
axes[0, 1].set_title('Volatility Over Time')
axes[0, 1].set_ylabel('Volatility')
axes[0, 1].legend()

# 3. Boxplot by day of week
sns.boxplot(x='day', y='volatility', data=data_df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ax=axes[1, 0])
axes[1, 0].set_title('Volatility by Day of the Week')
axes[1, 0].set_xlabel('Day')
axes[1, 0].set_ylabel('Volatility')

# 4. Bar chart of average volatility by hour
avg_vol_per_hour = data_df.groupby('hour')['volatility'].mean()
axes[1, 1].bar(avg_vol_per_hour.index, avg_vol_per_hour.values, color='purple')
axes[1, 1].set_title('Average Volatility by Hour of Day')
axes[1, 1].set_xlabel('Hour')
axes[1, 1].set_ylabel('Average Volatility')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
