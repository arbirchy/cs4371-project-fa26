import asyncio

import pyautogui as pya
import time
import pyperclip
import os
from translate import Translator
# from googletrans import Translator

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
                if "/data/" in  user_path:
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', user_path.replace("/data/","")))
                    print(file_path)
                else:
                    file_path = os.path.abspath(user_path)
                check_for_file(file_path)
                if check_for_file(file_path):
                    answers = open(file_path, "r").read()

            case "3":
                answers = input("Please enter your attack prompt here: ")

    return answers

def encoding_layer(attacks) -> str:
    auto_encode = input("\nWould you like to encode the inputs?\n1. Yes, translate to a language\n2. Yes, translate to Morse Code\n3. No, keep input raw\nPlease enter 1-3, here: ")
    match auto_encode:
        case "1":
            return auto_translate_language(attacks)
    return attacks

def auto_translate_language(attacks):
    language = input("Select a language:\n1. Italian\n2. Chinese \n3. Custom\nPlease enter 1-3, here: ")
    match language:
        case "1":
            lang = "it"
        case "2":
            lang = "zh"
        case "3":
            lang = input("Please enter the languages 2 letter ISO 639 code: ")
        case _:
            print("Invalid input, using Italian")
            lang = "it"
    for attack_num in range(len(attacks)):
        translator = Translator(to_lang=lang)
        translation = translator.translate(attacks[attack_num])
        print(translation)
        attacks[attack_num] = translation.replace("\'", "\\\'")
    write_to_file = input("Finished translating, write file to database under for future use?\ny or n: ")
    match write_to_file:
        case "y":
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'data', f'forbidden_questions_{lang}.csv'))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(attacks))
            print("File saved.")
    return attacks

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
        prompt = "First,"
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
    time.sleep(10)
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
attacks = encoding_layer(attacks)

print("\nAttack is ready to execute. After you press enter, you will have 5 seconds to switch to your attack window.")
input("Press enter to continue.")

time.sleep(5)

with open("output.csv", "w", encoding="utf-8") as f:
    for attack in attacks:
        result = perform_attack("level_2_attack_template.txt",attack)
        f.write(f"{result}\n")
        print(result)


