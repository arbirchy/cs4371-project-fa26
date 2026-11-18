import sys
import os
import json
from run_base import ask_openai, ask_claude, ask_gemini, load_questions_from_csv, load_level2_words

sys.path.insert(0, "Morse_Code_Translator")
import morsecode

def make_morse_levelOne(question):
    morse_question = morsecode.encrypt(question.upper()).strip()
    morse_first = morsecode.encrypt("FIRST").strip()
    return (
        "```python\n"
        f"question = '{morse_question}'\n"
        f"answer = '{morse_first}'\n"
        "```"
    )

questions = load_questions_from_csv()
print(make_morse_levelOne(questions[0]))