from fastapi import FastAPI
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# Function to fetch a meme from Reddit
def fetch_meme():
    url = "https://www.reddit.com/r/memes/top.json?limit=1"
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
        telex_api_url = "https://api.telex.im/v1/messages"
        headers = {"Authorization": "Bearer YOUR_TELEX_API_KEY"}
        data = {
            "channel_id": "meme-channel",
            "text": f"🕒 Hourly Meme: {meme_url}"
        }
        requests.post(telex_api_url, headers=headers, json=data)

# Schedule meme posting every hour
scheduler = BackgroundScheduler()
scheduler.add_job(post_meme_to_telex, 'interval', hours=1)
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