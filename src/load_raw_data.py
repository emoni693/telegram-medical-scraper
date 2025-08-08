import os
import json
import psycopg2
from config.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
cur = conn.cursor()

# Create raw schema and table
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN
);
""")
conn.commit()

data_dir = "data/raw/telegram_messages"
for date_folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, date_folder)
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
            messages = json.load(f)
            channel_name = file.replace(".json", "")
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (message_id, channel_name, message_date, message_text, has_media)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    msg["id"], channel_name, msg["date"], msg["text"], msg["media"]
                ))
conn.commit()
cur.close()
conn.close()
print("✅ Raw data loaded into PostgreSQL")
