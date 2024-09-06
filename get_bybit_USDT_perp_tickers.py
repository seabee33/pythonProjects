#simply list all bybit USDT perpetual tickers to import into trading view

import requests, json

url = "https://api.bybit.com/v5/market/tickers"
params = {"category": "linear",}
response = requests.get(url, params=params)

# Clear file
with open("bybit_tickers.txt","w") as f:
    f.write("")

# Write tickers 
data = response.json()
data = data["result"]["list"]
for item in data:
    if "USDT" in item["symbol"]:
        symbol = "BYBIT:" + item["symbol"] + ".P,"
        with open("bybit_tickers.txt", "a") as f:
            f.write(symbol)
