import pandas as pd

# 1. Load your current GitHub data (Save your pasted text as market_history.csv first)
file_name = 'market_history.csv'
df = pd.read_csv(file_name)

# 2. Ensure the time is recognized correctly
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 3. Sort by symbol and then by time (Crucial for matching history)
df = df.sort_values(['symbol', 'timestamp'])

# 4. Create the prev_price column by shifting within each symbol group
# This ensures AAPL's prev_price is its own previous price, not TSLA's.
df['prev_price'] = df.groupby('symbol')['price'].shift(1)

# 5. Fill the very first occurrence of each stock with its current price 
# (This prevents 'NaN' or empty cells in your dashboard)
df['prev_price'] = df['prev_price'].fillna(df['price'])

# 6. Sort it back to original chronological order for your dashboard
df = df.sort_values('timestamp')

# 7. Save the perfected file
df.to_csv(file_name, index=False)
print("Migration successful! New column 'prev_price' added and populated.")