#simply list all bybit USDT perpetual tickers to import into trading view

import requests, json

url = "https://api.bybit.com/v5/market/tickers"
params = {"category": "linear",}
response = requests.get(url, params=params)

data = response.json()
data = data["result"]["list"]
for item in data:
    print("BYBIT:" + item["symbol"] + ".P,")

with open("data.json", "a") as f:
    json.dump(data, f, indent=4)
