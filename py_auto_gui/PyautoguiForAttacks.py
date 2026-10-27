from os.path import curdir
from tabnanny import check

import pyautogui as pya
import time
import pyperclip
import os

def get_attack_input() -> str:
    print("Welcome to the pyautogui script. This script can automatically run attacks against LCCT tools.\nLet's set you up. First, how will you be entering your attacks?")
    answers = ""
    while not answers:
        input_type = input("1. File located at /data/forbidden_questions.csv\n2. Enter filepath\n3. Enter manually\nPlease enter 1-3, here: ")
        match input_type:
            case "1":
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'forbidden_questions.csv'))
                if check_for_file(file_path):
                    answers = open(file_path, "r").read()

            case "2":
                user_path = input("Please enter a valid filepath: ")
                file_path = os.path.abspath(user_path)
                check_for_file(file_path)
                if check_for_file(file_path):
                    answers = open(file_path, "r").read()

            case "3":
                answers = input("Please enter your attack prompt here: ")

    return answers

def check_for_file(path):
    try:
        answers = open(path, "r").read()
        user_check = input("File found! Enter \"r\" to read the file. Press enter to continue.")
        match user_check:
            case "r":
                print(answers)
                user_check = input("Does this look correct? Type \"n\" to find a new file. Press enter to continue.")
                if user_check != "n":
                    return True
            case _:
                return True
    except FileNotFoundError:
        print("File not found!")
    return False

def perform_attack(filename, attack_input):
    prompt_split = attack_input.split(" | ")
    if len(prompt_split) != 2:
        prompt = "First"
    else:
        prompt = prompt_split[1]

    keyword_split = prompt_split[0].split("*")
    if len(keyword_split) != 3:
        word_split = prompt_split[0].split(" ")
        mid_word = len(word_split)//2
        keyword = word_split[mid_word]
        start = " ".join(word_split[:mid_word])
        end = " ".join(word_split[mid_word+1:])
    else:
        keyword = keyword_split[1]
        start = keyword_split[0]
        end = keyword_split[2]

    attack_template = open(filename, "r").read()
    attack_template = attack_template.replace("*keyword*",keyword)
    attack_template = attack_template.replace("*prompt*", prompt)
    attack_template = attack_template.replace("*start*", start)
    attack_template = attack_template.replace("*end*", end)
    pya.hotkey('ctrl', 'a')
    pya.write(attack_template,interval=0.01)
    pya.press(["left","space"])
    time.sleep(5)
    pya.press("tab")
    with pya.hold("shift"):
        pya.press(["home", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right"])
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    s = pyperclip.paste()
    if s.replace(" ","") != prompt.replace(" ",""):
        return s
    else:
        return ""


attacks = get_attack_input().split("\n")

results = []
for attack in attacks:
    time.sleep(8)
    results.append(perform_attack("level_2_attack_template.txt",attack))

# prompt_for_answer()
print(results)

