import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_fetch import load_data_from_json
from data_preprocessing import preprocess_data
from pathlib import Path

json_path = Path(__file__).resolve().parent.parent / 'data' / 'AAPL_data.json'
data = load_data_from_json(json_path)
df = preprocess_data(data).sort_index()

# Calculate price change
df['price_change'] = df['close'].astype(float).diff()
df['abs_change'] = df['price_change'].abs()
df['hour'] = df.index.hour

#print("\n🔺 Top 5 positive price changes:")
#print(df[['close', 'price_change']].sort_values(by='price_change', ascending=False).head(5))

#print("\n🔻 Top 5 negative price changes:")
#print(df[['close', 'price_change']].sort_values(by='price_change').head(5))

plt.figure(figsize=(16, 10))

# Histogram of price changes
plt.subplot(2, 2, 1)
sns.histplot(df['price_change'].dropna(), bins=50, kde=True, color='skyblue')
plt.title("Distribution of Price Change")
plt.xlabel("Close Price Change")
plt.ylabel("Frequency")

# Line plot of price changes over time
plt.subplot(2, 2, 2)
df['price_change'].plot(color='orange')
plt.title("Price Change Over Time")
plt.ylabel("Change")
plt.xlabel("Time")

# Boxplot of price change by hour
plt.subplot(2, 1, 2)
sns.boxplot(x='hour', y='price_change', data=df)
plt.title("Price Change by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Price Change")

plt.tight_layout()
plt.show()
