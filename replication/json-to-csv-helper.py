import json
import csv
import os

with open("results.csv", 'w') as csvOutput:

    csvWriter = csv.writer(csvOutput)

    csvWriter.writerow(["Question",
                        "Model",
                        "Attack Level",
                        "Language",
                        "Prompt",
                        "Response",
                        "Refused?",
                        "Trial",
                        "Verdict",
                        "P(Safe)",
                        "P(Harmful)"])

    for dtory in ["results_initial", "results_italian", "results_morse", "results_chinese"]:
        langPlain = dtory[8:]
        print(langPlain)
        for file in os.scandir("./replication/" + dtory + "/probs"):
            with open(file, 'r') as currentJSONFile:
                currentJSON = json.load(currentJSONFile)
                for query in currentJSON:
                    csvWriter.writerow([query["question"],
                                        query["model"],
                                        query["level"],
                                        langPlain,
                                        query["prompt"],
                                        query["response"],
                                        query["refused"],
                                        query["trial"],
                                        query["verdict"],
                                        query["p_safe"],
                                        query["p_harmful"]])
                    
