import pandas as pd
import sys

for path in sys.argv[1:]:
    df = pd.read_json(path)
    df["harmful"] = df["verdict"] == "HARMFUL"

    per_trial = df.groupby(["model", "level", "trial"])["harmful"].mean() * 100
    print(per_trial.groupby(["model", "level"]).mean().round(1))