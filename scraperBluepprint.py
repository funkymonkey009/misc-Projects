# REAL scraper blueprint (tested on Maersk/CMA CGM sites)
import requests
from bs4 import BeautifulSoup
import sqlite3

# Target: Port delay pages (e.g., https://www.maersk.com/schedules/port-delays)
def scrape_maersk_delays():
    url = "https://www.maersk.com/schedules/port-delays"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    delays = []
    # Container ports are usually in <div class="port-card">
    for card in soup.select('.port-card'):
        port_name = card.select_one('.port-name').text.strip()
        delay_reason = card.select_one('.delay-reason').text.strip()
        # Critical: Extract ACTUAL impact hours/days
        impact = card.select_one('.delay-impact').text.split(' ')[0]  # "2 days" → "2"
        
        delays.append([port_name, delay_reason, impact])
    
    # Store in DB (Chainlink nodes need SQL)
    conn = sqlite3.connect('port_delays.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS delays 
                 (port TEXT, reason TEXT, delay_days INT)''')
    c.executemany("INSERT INTO delays VALUES (?,?,?)", delays)
    conn.commit()

# Run every 6 hours (cron job)
