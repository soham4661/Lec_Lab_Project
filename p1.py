from helpers import validate_quiz, grade_quiz

sample = [{"question": "2 + 2 = ?", "options": ["3", "4", "5", "22"],
           "correct_index": 1, "explanation": "Basic maths"}]
print(grade_quiz(sample, ["4"]))
print(grade_quiz(sample, ["22"]))
print(grade_quiz(sample, [None]))

