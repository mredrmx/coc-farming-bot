import time
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
from attack import attack_with_e_drags, attack_with_dragons
from dotenv import load_dotenv
import os

# --------------------------------------------- DE --------------------------------------------- #
# Die Main Logik hinter der Suchfunktion nach einer Base mit einer bestimmten Menge an Loot.
# Nutzt pytesseract für die OCR-Funktion (Text aus Screenshot vom Loot)
# Screenshot wird von pyautogui gemacht und dann mit cv2 bearbeitet
# Danach wird, je nach Account ("1" oder "2") mit dem "MIN_COMBINED_{ACCOUNT}" abgeglichen
# Ist genügend Loot vorhanden - > Angriff, ansonsten: Nächste Base

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic behind the search function for a base with a certain amount of loot.
# Uses pytesseract for the OCR function (text from screenshot of loot)
# Screenshot is taken by pyautogui and then processed with cv2
# Then, depending on the account (“1” or “2”) is compared with the “MIN_COMBINED_{ACCOUNT}”
# If there is enough loot - > attack, otherwise: next base

LOOKING_FOR_BASE = True
MIN_COMBINED_MAIN_ACCOUNT = 1800000  # 1.8 Million Elixir + Gold Combined
MIN_COMBINED_ALT_ACCOUNT = 600000  # 600K Elixir + Gold Combined
ATTACK_COUNTER = 0

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD") # YOUR Tesseract-OCR Filepath here
# Typically, it's installed in C:\Program Files\Tesseract-OCR or C:\Program Files (x86)\Tesseract-OCR


def searchforbase(user_account):
    global LOOKING_FOR_BASE
    LOOKING_FOR_BASE = True  # GANZ WICHTIG: immer wieder auf True setzen, bevor man startet!
    time.sleep(1)
    pyautogui.click(100, 1000)
    time.sleep(0.5)
    pyautogui.click(1400, 700)
    time.sleep(5)
    while LOOKING_FOR_BASE:
        path = os.getenv("SCREENSHOT_PATH") # YOUR path for the temporary screenshots here
        # Screenshot aufnehmen
        pyautogui.screenshot(path, region=(30, 120, 250, 130))

        # Screenshot laden und bearbeiten (HSV + Maske)
        cv2_image = cv2.imread(path)
        hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 60, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Maske in PIL-Image konvertieren für pytesseract
        mask_pil = Image.fromarray(mask)

        time.sleep(2)

        # OCR auf bearbeitetem Bild anwenden
        result = pytesseract.image_to_string(mask_pil, timeout=1, lang='eng',
                                             config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789')
        result = result.replace('\n\n', '\n')
        loot_list = result.splitlines()
        if user_account == "1":
            try:
                if MIN_COMBINED_MAIN_ACCOUNT <= int(loot_list[0]) + int(loot_list[1]) and int(loot_list[0]) < 2500000 and int(
                        loot_list[1]) < 2500000:
                    print(f"Found good base! Gold: {loot_list[0]}, Elixir: {loot_list[1]}")
                    LOOKING_FOR_BASE = False
                    attack_with_e_drags()  # Angriff starten
                    break  # GANZ WICHTIG: nach Angriff raus aus While-Loop!
                else:
                    pyautogui.click(x=1785, y=820)  # Nächste Base
                    time.sleep(5)
            except (ValueError, IndexError):
                pyautogui.click(x=1785, y=820)
                time.sleep(5)

        elif user_account == "2":
            try:
                if MIN_COMBINED_ALT_ACCOUNT <= int(loot_list[0]) + int(loot_list[1]) and int(loot_list[0]) < 400000 and int(
                        loot_list[1]) < 400000:
                    print(f"Found good base! Gold: {loot_list[0]}, Elixir: {loot_list[1]}")
                    LOOKING_FOR_BASE = False
                    attack_with_dragons()  # Angriff starten
                    break  # GANZ WICHTIG: nach Angriff raus aus While-Loop!
                else:
                    pyautogui.click(x=1785, y=820)  # Nächste Base
                    time.sleep(5)
            except (ValueError, IndexError):
                pyautogui.click(x=1785, y=820)
                time.sleep(5)

    LOOKING_FOR_BASE = True
