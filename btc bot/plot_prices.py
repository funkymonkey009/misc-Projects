import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "cryptodb"
DB_USER = "cryptouser"
DB_PASS = "raspberry"
DB_HOST = "localhost"

# Connect and fetch data
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
)
df = pd.read_sql("SELECT timestamp, price_usd FROM prices WHERE coin='bitcoin' ORDER BY timestamp", conn)
conn.close()

# Plot
plt.figure(figsize=(10,5))
plt.plot(df['timestamp'], df['price_usd'], marker='o')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.tight_layout()
plt.show()