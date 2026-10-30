model = "gemini-3.8-flash"
languages = ["English", "Hindi", "Hinglish"]
levels = ["Beginner", "Intermediate", "Advanced"]



chapter = {
    "type": "object",
    "properties": {
        "start": {"type": "string"},
        "heading": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["start", "heading", "key_points"],
}

key_term = {
    "type": "object",
    "properties": {
        "term": {"type": "string"},
        "definition": {"type": "string"},
    },
    "required": ["term", "definition"],
}

notes_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "chapters": {"type": "array", "items": chapter},
        "key_terms": {"type": "array", "items": key_term},
    },
    "required": ["title", "summary", "chapters", "key_terms"],
}



notes_prompt = (f"""You are notes maker having 15 yers of experience 
and a keen eye for detail and having a good understanding of the subject. 
Watch this lecture video and write study notes.

do follow these conditions:
- Use both what is said and what is shown (slides, code, whiteboard).
- Split the video into chapters in time order. Give each chapter its real start time as MM:SS or HH:MM:SS.
- Write 3 to 6 short key points for each chapter.
- List the key terms with a one-line definition for each.
- Write for a {levels} audience in {languages}.
- Include only what is in the video. Do not add outside information.
""")