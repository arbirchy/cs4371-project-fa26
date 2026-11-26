import asyncio
from fileinput import filename

import pyautogui as pya
import time
import pyperclip
import os
from translate import Translator
import sys

sys.path.append('../')
from Morse_Code_Translator import morsecode

# get_attack_input
#   inputs -> null
#   outputs -> String containing all attack prompts
#   description -> Offers the user different ways to input attack prompts
def get_attack_input() -> str:
    print("Welcome to the pyautogui script. This script can automatically run attacks against LCCT tools.\nLet's set you up. First, how will you be entering your attacks?")
    answers = ""
    while not answers:
        input_type = input("1. File located at /data/forbidden_questions.csv\n2. Enter filepath\n3. Enter manually\nPlease enter 1-3, here: ")
        # Check how user wants to input data
        match input_type:
            #Input from default file
            case "1":
                #Find the attack file
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'forbidden_questions.csv'))
                if check_for_file(file_path):
                    #Read from the attack file
                    answers = open(file_path, "r").read()

            #Input from different file
            case "2":
                user_path = input("Please enter a valid filepath: ")
                if "/data/" in  user_path:
                    #Likely files will be in /data. For convenience, we allow users to start their path with "/data/" to access this directory
                    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', user_path.replace("/data/","")))
                    print(file_path)
                else:
                    #If the user doesn't want a file from /data, they can enter an aboslute directory.
                    file_path = os.path.abspath(user_path)
                check_for_file(file_path)
                if check_for_file(file_path):
                    #Read from the attack file
                    answers = open(file_path, "r").read()

            #Input directly in console
            case "3":
                answers = input("Please enter your attack prompt here: ")

    return answers

# encoding_layer
#   inputs -> List[Strings] containing all attack prompts
#   outputs -> String containing encoded attack prompts
#   description -> Allows a user to encode attacks to a differnet language or morse code.
def encoding_layer(attacks) -> str:
    auto_encode = input("\nWould you like to encode the inputs?\n1. Yes, translate to a language\n2. Yes, translate to Morse Code\n3. No, keep input raw\nPlease enter 1-3, here: ")
    #Check if the user wants to encode inputs
    match auto_encode:
        #Encode to Language
        case "1":
            return auto_translate_language(attacks)
        #Encode to Morse
        case "2":
            for i_attack in range(len(attacks)):
                #Send each attack to the morse code translator.
                attacks[i_attack] = morsecode.encrypt(attacks[i_attack].upper())
                print("Morse: ", attacks[i_attack])
            #Allow the user to export to file to avoid encoding in the future.
            offer_output_file("forbidden_questions_morse.csv", "\n".join(attacks),"Would you like to save this file for future use?\n y or n: ")
            return attacks
    return attacks

# auto_translate_language
#   inputs -> String containing all attack prompts
#   outputs -> String containing encoded translated attack prompts
#   description -> Encodes attacks into a different language
def auto_translate_language(attacks):
    language = input("Select a language:\n1. Italian\n2. Chinese \n3. Custom\nPlease enter 1-3, here: ")
    #Allow user to choose language
    match language:
        #Itallian
        case "1":
            lang = "it"
        #Chinese
        case "2":
            lang = "zh"
        #Any language
        case "3":
            lang = input("Please enter the languages 2 letter ISO 639 code: ")
        case _:
            print("Invalid input, using Italian")
            lang = "it"
    for attack_num in range(len(attacks)):
        #Send each attack to translator API
        translator = Translator(to_lang=lang)
        translation = translator.translate(attacks[attack_num])
        print(translation)
        attacks[attack_num] = translation.replace("\'", "\\\'")
    #Allow user to output to file to avoid re-translating in the future.
    offer_output_file(f'forbidden_questions_{lang}.csv',"\n".join(attacks), "Finished translating, write file to database under for future use?\ny or n: ")
    return attacks

# offer_output_file
#   inputs:
#       filename -> name of the file to output
#       content -> content to write into file
#       msg -> Message to display to user when asking if they want to safe the file
#   outputs -> null
#   description -> Util function to quickly save files that the user may want to use later.
def offer_output_file(filename, content, msg):
    write_to_file = input(msg)
    #Ask if the user wants to save the file
    match write_to_file:
        case "y":
            #Save to data path
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'data', f'{filename}'))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("File saved.")

# check_for_file
#   inputs -> String containing a path
#   outputs -> Bool on whether the file exists or not
#   description -> Checks if a file exists at a specific path, allowing users to check if it is the correct file.
def check_for_file(path):
    try:
        #Read file content
        answers = open(path, "r").read()
        user_check = input("File found! Enter \"r\" to read the file. Press enter to continue.")
        #Allow user to read file
        match user_check:
            case "r":
                #Print out file content for user to read
                print(answers)
                user_check = input("Does this look correct? Type \"n\" to find a new file. Press enter to continue.")
                if user_check != "n":
                    #If correct file, return True
                    return True
            case _:
                return True
    except FileNotFoundError:
        print("File not found!")
    #Either no file, or incorrect file
    return False

# perform_attack_level_2
#   inputs:
#       filename -> String containing path to the template to use for the attack
#       attack_input -> String containing the attack prompt
#       prompt -> String containing the text that will prompt the model
#   outputs -> String containing the models output message (or empty string for no response)
#   description -> Runs a level 2 attack against the LCCT model.
def perform_attack_level_2(filename, attack_input, prompt):

    #If the prompt has a | character, use it as the prompt
    prompt_split = attack_input.split(" | ")
    if len(prompt_split) == 2:
        prompt = prompt_split[1]

    #If the prompt has a word surrounded by '*', use it as the keyword in the attack
    keyword_split = prompt_split[0].split("*")
    if len(keyword_split) == 3:
        keyword = keyword_split[1]
        start = keyword_split[0]
        end = keyword_split[2]
        
    #Else, just use the middle word as the keyword
    else:
        word_split = prompt_split[0].split(" ")
        mid_word = len(word_split)//2
        keyword = word_split[mid_word]
        start = " ".join(word_split[:mid_word])
        end = " ".join(word_split[mid_word+1:])

    #Open the attack template and replace all the placeholders with the attack inputs
    attack_template = open(filename, "r").read()
    attack_template = attack_template.replace("*keyword*",keyword)
    attack_template = attack_template.replace("*prompt*", prompt)
    attack_template = attack_template.replace("*start*", start)
    attack_template = attack_template.replace("*end*", end)
    #Highlight all the current text
    pya.hotkey('ctrl', 'a')
    #Write the attack file
    pya.write(attack_template,interval=0.01)
    #Write a space into the string to prompt the model to auto complete
    pya.press(["left","space"])
    #Wait for the model to auto complete
    time.sleep(10)
    #Press tab to accept models output
    pya.press("tab")
    #Highlight the models output
    with pya.hold("shift"):
        pya.press(["home", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right"])
    #Copy the models output
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    #Get the models output
    s = pyperclip.paste()
    #If model successfully output a response, return it
    if s.replace(" ","") != prompt.replace(" ",""):
        return s
    #Else, return an empty string
    else:
        return ""

# perform_attack_level_1
#   inputs:
#       attack_input -> String containing the attack prompt
#       prompt -> String containing the text that will prompt the model
#   outputs -> String containing the models output message (or empty string for no response)
#   description -> Runs a level 1 attack against the LCCT model.
def perform_attack_level_1(attack_input, prompt):
    # Highlight all text
    pya.hotkey('ctrl', 'a')
    #Write in the attack
    pya.write(attack_input.replace(" ", "_").lower() + f" = \"{prompt}\"", interval=0.01)
    #Write a space into the string to prompt the model to auto complete
    pya.press(["left", "space"])
    #Wait for the model to auto complete
    time.sleep(10)
    #Press tab to accept models output
    pya.press("tab")
    #Highlight the models output
    with pya.hold("shift"):
        pya.press("home")
        with pya.hold("ctrl"):
            pya.press(["right", "right"])
        pya.press(["right","right"])
    #Copy the models output
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    #Get the models output
    s = pyperclip.paste()
    #If model successfully output a response, return it
    if s.replace(" ", "") != prompt.replace(" ", ""):
        return s
    #Else, return an empty string
    else:
        return ""

#Get string of attacks and split it into a list of attacks
attacks = get_attack_input().split("\n")
#Encode the attacks
attacks = encoding_layer(attacks)

#Offer the option to decode the models output
decode = input("\nShould the output be decoded?\n1. No, plain text only\n2. Yes, translate back to English\n3. Yes, decrypt morse code\nPlease enter 1-3, here: ")

#Ask the user what prompt should be used on the model
prompt = input("What prompt should be used: ")
if prompt == "": prompt = "First,"

#Ask the user what attack type should be used
attack_type = input("What attack type?\n1. Level 1 attack\n2. Level 2 attack\n")

print("\nAttack is ready to execute. After you press enter, you will have 5 seconds to switch to your attack window.")
input("Press enter to continue.")

time.sleep(5)

#Write each result to an output file to ensure data isn't lost if program prematurely stops
with open("output.csv", "w", encoding="utf-8") as f:
    for attack in attacks:
        #Run attack according to its type
        match attack_type:
            case "1":
                raw_result = perform_attack_level_1(attack,prompt)
            case _:
                raw_result = perform_attack_level_2("level_2_attack_template.txt", attack, prompt)
        #Decode attack
        match decode:
            #Translate back to English
            case "2":
                #Use a try. In the case of error (API down, no credits, etc) program should still continue
                try:
                    translator = Translator(to_lang="en")
                    decrypted_result = translator.translate(raw_result)
                except:
                    decrypted_result = ""
            #Decode morse code
            case "3":
                try:
                    decrypted_result = morsecode.decrypt(raw_result)
                except:
                    decrypted_result = ""
            case _:
                decrypted_result = raw_result
        #Write results to output file
        f.write(f"{attack}~~{raw_result}~{decrypted_result}\n")
        print(f"{attack},{raw_result},{decrypted_result}\n")


