from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import feedparser

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 信頼できるNitterインスタンス
NITTER_URL = "https://lightbrd.com/"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/view/{username}")
async def view_tweets(request: Request, username: str):
    # RSSフィードの取得
    rss_url = f"{NITTER_URL}/{username}/rss"
    feed = feedparser.parse(rss_url)
    
    posts = []
    for entry in feed.entries:
        posts.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.published,
            "description": entry.description  # HTML形式の本文
        })
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "posts": posts, 
        "username": username
    })
