from google import genai
from dotenv import load_dotenv
import streamlit as st
import time

load_dotenv()
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "text", "text": "Please summarize the video in 3 sentences."},
        {"type": "video", "uri": "https://youtu.be/qy7vHLyVBAc?si=_lmHPT_mO3cWNQai"}
    ]
)
print(interaction.output_text)