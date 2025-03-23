import matplotlib.pyplot as plt
import seaborn as sns
from data_fetch import load_data_from_json
from data_preprocessing import preprocess_data
from pathlib import Path

json_path = Path(__file__).resolve().parent.parent / 'data' / 'AAPL_data.json'
raw_data = load_data_from_json(json_path)

if raw_data is None:
    print("Error loading data. Exiting.")
    exit()

data_df = preprocess_data(raw_data)
data_df = data_df.sort_index()
data_df['close'] = data_df['close'].astype(float)

#print("\n Basic statistics for `close` price:\n")
#print(data_df['close'].describe())

#print("\n Skewness:", round(data_df['close'].skew(), 4))
#print(" Kurtosis:", round(data_df['close'].kurtosis(), 4))

#Identify outliers
data_df['anomaly'] = data_df['z_score'].abs() > 2
outliers = data_df[data_df['anomaly'] == True]

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=False)

# Top plot: histogram with KDE
sns.histplot(data_df['close'], bins=40, kde=True, ax=axes[0], color='steelblue')
axes[0].set_title('Distribution of Close Prices')
axes[0].set_xlabel('Close Price')
axes[0].set_ylabel('Frequency')
axes[0].grid(True)

# Bottom plot: line chart with SMA and outliers
axes[1].plot(data_df.index, data_df['close'], label='Close', color='steelblue')
axes[1].plot(data_df.index, data_df['sma_50'], label='SMA 50', color='orange')
axes[1].scatter(outliers.index, outliers['close'], color='red', label='Outlier', zorder=5)
axes[1].set_title('Close Prices Over Time with SMA and Outliers')
axes[1].set_ylabel('Close Price')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()
