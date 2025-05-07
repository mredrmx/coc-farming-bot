import random
import time
import pyautogui
from attacks_by_position import e_drags_top_left, e_drags_top_right, e_drags_bottom_left, \
    e_drags_bottom_right, dragons_top_right, dragons_top_left, dragons_bottom_right, \
    dragons_bottom_left

# --------------------------------------------- DE --------------------------------------------- #
# Die Main Logik hinter den Angriffen, falls eine Base gefunden wurde.
# Es wird eine Random Attack Position aus "attack_positions" gewählt und, je nach Position und Account, angegriffen.
# Die Attacks sind der Übersicht halber aus "AttacksByPosition" importiert (viel nervige Handarbeit/Ausprobieren)

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic behind the attacks, if a base has been found.
# A random attack position is selected from “attack_positions” and, depending on the position and account, attacked.
# The attacks are imported from “AttacksByPosition” for the sake of clarity (a lot of annoying
# manual work/trial and error)


# Random Attack Positions
attack_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]


# Für den Account "Saint"
def attack_with_e_drags():
    start_position = random.choice(attack_positions)
    if start_position == "top_left":
        e_drags_top_left()
    elif start_position == "top_right":
        e_drags_top_right()
    elif start_position == "bottom_left":
        e_drags_bottom_left()
    elif start_position == "bottom_right":
        e_drags_bottom_right()
    print("Angriff beendet.")
    pyautogui.click(150, 850)
    time.sleep(0.3)
    pyautogui.click(1170, 700)
    time.sleep(0.3)
    pyautogui.click(960, 930)
    time.sleep(2)


# Für den Account "Hero"
def attack_with_dragons():
    start_position = random.choice(attack_positions)
    if start_position == "top_left":
        dragons_top_left()
    elif start_position == "top_right":
        dragons_top_right()
    elif start_position == "bottom_left":
        dragons_bottom_left()
    elif start_position == "bottom_right":
        dragons_bottom_right()
    print("Angriff beendet.")
    pyautogui.click(150, 850)
    time.sleep(0.3)
    pyautogui.click(1170, 700)
    time.sleep(0.3)
    pyautogui.click(960, 930)
    time.sleep(2)
