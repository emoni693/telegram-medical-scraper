from fastapi import FastAPI, HTTPException
from typing import List
from schemas import TopProduct, ChannelActivity, MessageSearchResult
import crud

app = FastAPI()

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10):
    results = crud.get_top_products(limit)
    return results

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str):
    results = crud.get_channel_activity(channel_name)
    if not results:
        raise HTTPException(status_code=404, detail="Channel not found")
    return results

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_messages(query: str):
    results = crud.search_messages(query)
    return results
@app.get("/")
def read_root():
    return {"message": "Telegram Medical Scraper API is running!"}