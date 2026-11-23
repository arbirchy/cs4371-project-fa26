import sys
import os
import json
import csv
from run_base import ask_openai, ask_claude, ask_gemini, load_questions_from_csv, make_levelTwo

def load_chinese_questions():
    questions = []
    with open("data/forbidden_questions_chi.csv", encoding="utf-8") as f:
        for row in csv.reader(f):
            questions.append(row[0])
    return questions


def make_chinese_levelOne(question):
    question = question.lower()
    question = question.replace("come ", "")
    name = question.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.replace("\\'", "_")
    return f"```python\n{name} = 'First'\n```"


def load_chinese_words():
    words = {}
    with open("data/level2_words_chi.csv", encoding="utf-8") as f:
        for row in csv.reader(f):
            words[row[0]] = row[1]
    return words


if __name__ == '__main__':
    english = load_questions_from_csv()
    chinese = load_chinese_questions()
    words = load_chinese_words()
    trials = 1 # Only one trial b cuz I am broke :/ 
    models = sys.argv[1:]
    os.makedirs("replication/results_chinese", exist_ok=True)
    for model in models:
        path = f"replication/results_chinese/results_chinese_{model}.json"
        results = []
        done = set()
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                results = json.load(f)
            for r in results:
                done.add((r["trial"], r["question"], r["level"]))
            print("Resuming", model, "with", len(results), "done")
        for trial in range(1, trials + 1):
            for question, question_it in zip(english, chinese):
                for level in [1,2]:
                    if (trial, question, level) in done:
                        continue
                    if level == 1:
                        prompt = make_chinese_levelOne(question_it)
                    else:
                        prompt = make_levelTwo(question_it, words[question])
                    if model.startswith("claude"):
                        text, refused = ask_claude(model, prompt)
                    elif model.startswith("gemini"):
                        text, refused = ask_gemini(model, prompt)
                    else:
                        text, refused = ask_openai(model, prompt)
                    results.append({
                        "question": question,
                        "question_it": question_it,
                        "model": model,
                        "level": level,
                        "prompt": prompt,
                        "response": text,
                        "refused": refused,
                        "trial": trial,
                    })
                    print("MODEL:", model)
                    print("QUESTION:", question_it)
                    print("LEVEL:", level)
                    print("REFUSED:", refused)
                    print(text)
                    print("--------------------")
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2)