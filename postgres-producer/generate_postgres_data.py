import psycopg2
from datetime import datetime, timedelta
import random
import uuid
import os

# DB connection settings
DB_NAME = os.getenv("DB_NAME", "airflow")
DB_USER = os.getenv("DB_USER", "airflow")
DB_PASS = os.getenv("DB_PASS", "airflow")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))


# Sample data options
EVENT_TYPES = ['login', 'purchase', 'logout', 'click']
LOCATIONS = ['Helsinki', 'Stockholm', 'Oslo', 'Berlin', 'Copenhagen']

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id UUID PRIMARY KEY,
            user_id TEXT,
            event_type TEXT,
            timestamp TIMESTAMP,
            location TEXT
        );
    """)

def insert_fake_data(cursor, num_rows=500):
    now = datetime.utcnow()
    for _ in range(num_rows):
        id = str(uuid.uuid4())
        event = {
            "id": id,
            "user_id": f"user_{random.randint(1, 100)}",
            "event_type": random.choice(EVENT_TYPES),
            "timestamp": now - timedelta(minutes=random.randint(0, 1440)),
            "location": random.choice(LOCATIONS)
        }
        cursor.execute("""
            INSERT INTO events (id, user_id, event_type, timestamp, location)
            VALUES (%(id)s, %(user_id)s, %(event_type)s, %(timestamp)s, %(location)s);
        """, event)
        print(f"Sample record with id = {id} inserted into PostgreSQL.")

def main():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    create_table(cursor)
    insert_fake_data(cursor, num_rows=500)

    print("Sample data inserted into PostgreSQL.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
