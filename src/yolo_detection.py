import os
from ultralytics import YOLO
import psycopg2
from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

model = YOLO("yolov8n.pt")  # Small pre-trained YOLOv8 model

conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
cur = conn.cursor()

cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.image_detections (
    detection_id SERIAL PRIMARY KEY,
    message_id BIGINT,
    detected_object_class TEXT,
    confidence_score FLOAT
);
""")
conn.commit()

image_dir = "data/raw/telegram_images"
for channel in os.listdir(image_dir):
    for img in os.listdir(os.path.join(image_dir, channel)):
        img_path = os.path.join(image_dir, channel, img)
        results = model(img_path)
        for r in results:
            for box in r.boxes:
                cls = model.names[int(box.cls)]
                conf = float(box.conf)
                # Assuming image filename starts with message_id
                message_id = int(img.split("_")[0]) if img.split("_")[0].isdigit() else None
                cur.execute("""
                    INSERT INTO raw.image_detections (message_id, detected_object_class, confidence_score)
                    VALUES (%s, %s, %s)
                """, (message_id, cls, conf))
conn.commit()
cur.close()
conn.close()
print("✅ YOLO detections saved to database")
