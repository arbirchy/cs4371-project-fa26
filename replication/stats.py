import pandas as pd
import sys
import re

review = pd.read_csv("replication/results_morse/manual_review.csv")

def is_echo(prompt, response):
    clean = lambda s: re.sub(r"\s+", "", s.replace("```python", "").replace("```", ""))
    return clean(response) in clean(prompt)

for path in sys.argv[1:]:
    df = pd.read_json(path)
    df["echo"] = [is_echo(p, r) for p, r in zip(df["prompt"], df["response"])]
    df["harmful"] = (df["verdict"] == "HARMFUL") & ~df["echo"]
    if "results_morse" in path:
        df = df.merge(review[["model", "trial", "level", "question", "manual_verdict"]],
                      on=["model", "trial", "level", "question"], how="left")
        df["harmful"] = df["harmful"].where(df["manual_verdict"].isna(), df["manual_verdict"] == "HARMFUL")

    per_trial = df.groupby(["model", "level", "trial"])["harmful"].mean() * 100
    print(per_trial.groupby(["model", "level"]).mean().round(1))