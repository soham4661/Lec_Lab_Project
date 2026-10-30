import time
from google import genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = genai.Client()






interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain how AI works in a few words"
)