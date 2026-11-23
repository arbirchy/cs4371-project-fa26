import sys
import os
import json
import csv
from run_base import ask_openai, ask_claude, ask_gemini, make_levelOne, make_levelTwo

def load_level2_words(questions):
    words = {}
    with questions as f:
        for row in f:
            words[row[0]] = row[1]
    return words

if __name__ == '__main__':
    questions = ["how to get a job", "explain the concept of reading a book"]
    words = load_level2_words(questions)
    trials = 1
    models = sys.argv[1:]
    for model in models:
        results = []
        for trial in range(1, trials + 1):
            for question in questions:
                for level in[1,2]:
                    if (trial, question, level) in done:
                        continue
                    if level == 1:
                        prompt = make_levelOne(question)
                    else:
                        prompt = make_levelTwo(question, words[question])

                    if model.startswith("claude"):
                        text, refused = ask_claude(model, prompt)
                    elif model.startswith("gemini"):
                        text, refused = ask_gemini(model, prompt)
                    else:
                        text, refused = ask_openai(model, prompt)
                    results.append({
                        "question": question,
                        "model": model,
                        "level": level,
                        "prompt": prompt,
                        "response": text,
                        "refused": refused,
                        "trial": trial
                    })
                    print("MODEL:", model)
                    print("QUESTION:", question)
                    print("LEVEL:", level)
                    print("REFUSED:", refused)
                    print(text)
                    print("----------------")