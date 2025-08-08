from telethon import TelegramClient
import os
import json
from datetime import datetime
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE
from logger import logger

client = TelegramClient("scraper", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def scrape_channel(channel):
    logger.info(f"Starting to scrape: {channel}")
    await client.start(phone=TELEGRAM_PHONE)  # use preloaded phone number
    messages = []

    async for message in client.iter_messages(channel, limit=1000):
        data = {
            "id": message.id,
            "date": str(message.date),
            "text": message.text,
            "media": bool(message.media)
        }
        messages.append(data)

        if message.media:
            folder = f"data/raw/telegram_images/{channel.replace('https://t.me/', '')}"
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"{message.id}")
            await message.download_media(file=filename)

    date_folder = datetime.now().strftime("%Y-%m-%d")
    save_path = f"data/raw/telegram_messages/{date_folder}"
    os.makedirs(save_path, exist_ok=True)

    with open(f"{save_path}/{channel}.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    logger.info(f"Finished scraping: {channel}")

async def main():
    channels = [
        "lobelia4cosmetics",
        "tikvahpharma"
    ]
    for ch in channels:
        await scrape_channel(ch)

with client:
    client.loop.run_until_complete(main())
