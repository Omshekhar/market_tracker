import requests 
import pandas as pd
from datetime import datetime
import os

API_KEY = '3B1B82I1PBCG8JPP'
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
FILE_NAME = 'market_history.csv'

def fetch_data(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url, timeout=10).json()
        return response.get('Global Quote', {})
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {}

# 1. Load existing data
if os.path.exists(FILE_NAME):
    df_old = pd.read_csv(FILE_NAME)
else:
    # Create empty dataframe with the new column structure if file doesn't exist
    df_old = pd.DataFrame(columns=['timestamp', 'symbol', 'price', 'volume', 'prev_price'])

def get_prev_price(symbol, current_price):
    # Filter the old data for this specific symbol
    last_entries = df_old[df_old['symbol'] == symbol]
    if not last_entries.empty:
        return last_entries['price'].iloc[-1]
    # If no history exists, use current_price so the "Change" is 0 instead of a broken number
    return current_price

# 2. Fetch new data
records = []
for s in SYMBOLS:
    res = fetch_data(s)
    if res and '05. price' in res:
        new_price = float(res['05. price'])
        new_volume = int(res['06. volume'])
        symbol = res['01. symbol']
        
        # Get the previous price
        prev_price = get_prev_price(symbol, new_price)

        # Logic Gate: Check the last recorded entry to avoid duplicates
        last_entry_match = df_old[df_old['symbol'] == symbol].tail(1)
        if not last_entry_match.empty:
            last_price = float(last_entry_match['price'].values[0])
            last_volume = int(last_entry_match['volume'].values[0])
            
            # Only skip if BOTH price and volume are identical to the last check
            if new_price == last_price and new_volume == last_volume:
                print(f"Skipping {symbol}: No market movement.")
                continue

        # Append the new record
        records.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol,
            'price': new_price,
            'volume': new_volume,
            'prev_price': prev_price
        })

# 3. Save only if we have new records
if records:
    df_new = pd.DataFrame(records)
    # Combine old data with new records
    df_final = pd.concat([df_old, df_new], ignore_index=True)
    # Write the full updated file back to CSV
    df_final.to_csv(FILE_NAME, index=False)
    print(f"Logged {len(records)} new unique records.")
else:
    print("No new market data to log.")