def youtube_id(url):
    url = url.strip()
    markers = ["watch?v=", "youtu.be/", "/shorts/"]

    found_marker = None
    for marker in markers:
        if marker in url:
            found_marker = marker
            break

    if found_marker is None:
        return None

    after_marker = url.split(found_marker)[1]
    video_id = after_marker[:11]

    if len(video_id) == 11:
        return video_id
    else:
        return None



#code for good quizgeneration:

def validate_quiz(questions):
    good_questions = []
    problems = []

    for number, q in enumerate(questions, start=1):
        if len(q["options"]) != 4:
            problems.append(f"Q{number}: has {len(q['options'])} options (expected 4)")
            continue

        if q["correct_index"] not in [0, 1, 2, 3]:
            problems.append(f"Q{number}: correct_index {q['correct_index']} is out of range")
            continue

        cleaned = set(o.strip() for o in q["options"])
        if len(cleaned) < 4:
            problems.append(f"Q{number}: has same or empty options")
            continue

        good_questions.append(q)

    return good_questions, problems

# Grade_Quiz
def grade_quiz(questions,answers):
    score = 0
    results = []

    for question,answer in zip(questions,answers):
        correct = question["options"][question["correct_index"]]

        if answer == correct:
            score = score + 1
            is_correct = True
        else:
            is_correct = False

        results.append({"chosen": answer, "correct": correct, "is_correct": is_correct})

    return score, results

# Error Hnadling
def friendly_error(error):
    msg = str(error).lower()

    if "429" in msg or "quota" in msg or "resource_exhausted" in msg:
        return "Too many requests. Wait a minute and  try again."
    


















       



#def youtube_id(url):
    #url = url.strip()

    #if "watch?v=" in url:
    #    part = url.split("watch?v=")[1]
    #elif "youtu.be/" in url:
      #  part = url.split("youtu.be/")[1]
    #elif "/shorts/" in url:
     #   part = url.split("/shorts/")[1]
    #else:
     #   return None

    #video_id = part[:11]

    #if len(video_id) == 11:
     #   return video_id
    #else:
     #   return None