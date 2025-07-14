from flask import Flask, render_template_string
import psycopg2
import pandas as pd

app = Flask(__name__)

DB_NAME = "cryptodb"
DB_USER = "cryptouser"
DB_PASS = "raspberry"
DB_HOST = "localhost"

@app.route('/')
def index():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    df = pd.read_sql("SELECT timestamp, price_usd FROM prices WHERE coin='bitcoin' ORDER BY timestamp DESC LIMIT 20", conn)
    conn.close()
    table_html = df.to_html(index=False)
    return render_template_string("""
        <h1>Bitcoin Price Tracker</h1>
        <p>Last 20 entries:</p>
        {{table|safe}}
    """, table=table_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)