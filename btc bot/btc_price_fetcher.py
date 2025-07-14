import requests
import psycopg2
from datetime import datetime

# Database connection details
DB_NAME = "cryptodb"
DB_USER = "cryptouser"
DB_PASS = "raspberry"
DB_HOST = "localhost"

# Fetch Bitcoin price from CoinGecko
url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
response = requests.get(url)
data = response.json()
price = data['bitcoin']['usd']
timestamp = datetime.now()

# Connect to PostgreSQL and insert data
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
)
cur = conn.cursor()
cur.execute(
    "INSERT INTO prices (timestamp, coin, price_usd) VALUES (%s, %s, %s)",
    (timestamp, 'bitcoin', price)
)
conn.commit()
cur.close()
conn.close()

print(f"Inserted Bitcoin price: ${price} at {timestamp}")

with open("/home/pi/btc_price_fetcher.log", "a") as log:
    log.write(f"Fetched at {timestamp}, price: {price}\n")
