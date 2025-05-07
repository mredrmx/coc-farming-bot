import time
import random
import pyautogui
import pygetwindow
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
from attack import attack
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = r"C:\Users\jojow\Pictures\TEST\test.png"
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

print(loot_list)