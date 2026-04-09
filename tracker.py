import requests 
import pandas as pd
from datetime import datetime

API_KEY = '3B1B82I1PBCG8JPP'  # Replace with your actual Alpha Vantage API key
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # List of stock symbols to track

def fetch_data(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url).json() 
    data = response.get('Global Quote', {})
    return data

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