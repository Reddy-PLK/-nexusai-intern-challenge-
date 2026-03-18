import sqlite3
from datetime import datetime

# connect to database (creates file if not exists)
conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    message TEXT,
    response TEXT,
    timestamp TEXT
)
""")

conn.commit()


# function to save message
def save_message(customer_id, message, response):
    timestamp = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO messages (customer_id, message, response, timestamp)
    VALUES (?, ?, ?, ?)
    """, (customer_id, message, response, timestamp))

    conn.commit()