from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "text", "text": "Please summarize the video in 3 sentences."},
        {"type": "video", "uri": "https://www.youtube.com/watch?v=9hE5-98ZeCg"}
    ]
)
print(interaction.output_text)