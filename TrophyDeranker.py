import random
import time
import pyautogui

# --------------------------------------------- DE --------------------------------------------- #
# Macht, was der Name sagt: Trophies deranken (Match finden, Zap usen, aufgeben, repeat;
# Läuft so oft, bis "Counter" erreicht ist

# --------------------------------------------- ENG --------------------------------------------- #
# Does what the name says: Trophies derank (find match, zap, give up, repeat;
# Runs until “Counter” is reached

counter = 0
time.sleep(5)
while counter < 30:
    time.sleep(1)
    pyautogui.click(100, 1000)
    time.sleep(0.5)
    pyautogui.click(1400, 700)
    time.sleep(4)
    pyautogui.click(1100, 1000)
    pyautogui.click(960 + random.randint(-150, 150), 540 + random.randint(-150, 150))
    time.sleep(random.randint(1, 2))
    pyautogui.click(150, 850)
    time.sleep(random.uniform(0.3, 0.8))
    pyautogui.click(1170, 700)
    time.sleep(random.uniform(0.4, 0.7))
    pyautogui.click(960, 930)
    time.sleep(1.5)
    counter += 1
