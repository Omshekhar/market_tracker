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

# 1. Load existing data to check for duplicates
if os.path.exists(FILE_NAME):
    existing_df = pd.read_csv(FILE_NAME)
else:
    existing_df = pd.DataFrame(columns=['timestamp', 'symbol', 'price', 'volume'])

records = []
for s in SYMBOLS:
    res = fetch_data(s)
    if res and '05. price' in res:
        new_price = float(res['05. price'])
        new_volume = int(res['06. volume'])
        symbol = res['01. symbol']
        
        # 2. Logic Gate: Check the last recorded entry for THIS symbol
        last_entry = existing_df[existing_df['symbol'] == symbol].tail(1)
        
        if not last_entry.empty:
            last_price = float(last_entry['price'].values[0])
            last_volume = int(last_entry['volume'].values[0])
            
            # Only append if price or volume has changed
            if new_price == last_price and new_volume == last_volume:
                print(f"Skipping {symbol}: No market movement.")
                continue 
        
        records.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol,
            'price': new_price,
            'volume': new_volume
        })

# 3. Save only if we have new records
if records:
    df = pd.DataFrame(records)
    df.to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False)
    print(f"Logged {len(records)} new unique records.")
else:
    print("No new market data to log.")
# Process and Save
records = []
for s in SYMBOLS:
    res = fetch_data(s)
    if res:
        records.append({
            'timestamp': datetime.now(),
            'symbol': res['01. symbol'],
            'price': float(res['05. price']),
            'volume': int(res['06. volume'])
        })

df = pd.DataFrame(records)
df.to_csv('market_history.csv', mode='a', header=not pd.io.common.file_exists('market_history.csv'), index=False)
print("Data logged successfully!")
