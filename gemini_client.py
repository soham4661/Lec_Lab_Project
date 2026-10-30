import os
import json
import time
from dotenv import load_dotenv
from google import genai
from config import MODEL


def get_client():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)


def video_part(youtube_link):
    return {"type": "video", "uri": youtube_link}

















def video_part(youtube_link):
    return {"type": "video", "uri": youtube_link}

print(video_part("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))