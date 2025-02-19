from fastapi import FastAPI
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
TELEX_API_URL = os.getenv("TELEX_URL")

# Function to fetch a meme from Reddit
def fetch_meme():
    url = "https://www.reddit.com/r/memes/new.json?limit=1"
    headers = {"User-Agent": "MemeOfTheHour/1.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        meme_url = data["data"]["children"][0]["data"]["url"]
        return meme_url
    return None

# Function to post meme to Telex
def post_meme_to_telex():
    meme_url = fetch_meme()
    if meme_url:
        payload = {
            "event_name": "😂 Hourly Meme: ",
            "message": f"😂{meme_url}",
            "status": "success",
            "username": "💀meme-bot",
            }

        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
        
        response = requests.post(TELEX_API_URL, headers=headers, json=payload)
        print(response.json())

# Schedule meme posting every hour
scheduler = BackgroundScheduler()
scheduler.add_job(post_meme_to_telex, 'interval', minutes=1)
scheduler.start()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to MemeOfTheHour!"}

# Meme endpoint
@app.get("/meme")
def get_meme():
    meme_url = fetch_meme()
    if meme_url:
        return {"meme_url": meme_url}
    return {"error": "Failed to fetch meme"}