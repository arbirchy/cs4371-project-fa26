import pyautogui as pya
import time
import pyperclip

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

time.sleep(5)

prompt_for_answer()