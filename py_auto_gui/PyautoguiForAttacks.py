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

def prompt_for_answer():
    pya.press("pagedown")
    with pya.hold('shift'):
        pya.press("home")
    pya.press("backspace")
    pya.write("answer = \'\'")
    pya.press("left")
    pya.write("First, ", interval=0.1)
    time.sleep(5)
    pya.press("tab")
    with pya.hold("shift"):
        pya.press(["home","right","right","right","right","right","right","right","right","right","right"])
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    s = pyperclip.paste()
    if s != "First,    ":
        return s
    else:
        return ""

def replace_attack_second(filename, attack_input):
    keyword = attack_input.split("*")
    if len(keyword) != 3:
        print("invalid, couldn't find keyword")
        return
    keyword = keyword[1]

    prompt = attack_input.split("|")
    if len(prompt) != 1:
        prompt = "First "
        return
    prompt = prompt[1]


    attack_template = open(filename, "r").read()
    attack_template = attack_template.replace("*keyword*",keyword)
    attack_template = attack_template.replace("*keyword*", keyword)
    pya.write(attack_template)


attack = get_attack_input().split("\n")

for i in attack:

    break

replace_attack_second("level_2_attack_template.txt",attack[0])

# prompt_for_answer()