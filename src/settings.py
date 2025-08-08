from dotenv import load_dotenv 
import os

load_dotenv()

TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")         # ✅ Add this
POSTGRES_HOST = os.getenv("POSTGRES_HOST")     # ✅ Add this
POSTGRES_PORT = os.getenv("POSTGRES_PORT")     # ✅ Add this
