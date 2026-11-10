from Training_Python_Beginner.Lec_Labs_prj.gemini_client import call_gemini
from config import FLASHCARD_PROMPT, FLASHCARD_SCHEMA, MODEL, languages, levels, NOTES_PROMPT, NOTES_SCHEMA
import json


def make_flashcards(client, notes, count, language, log):
    notes_text = json.dumps(notes)
    prompt = FLASHCARD_PROMPT.format(count=count, language=language, notes=notes_text)
    result = call_gemini(client, prompt, log, "flashcards", FLASHCARD_SCHEMA)
    return result["cards"]
