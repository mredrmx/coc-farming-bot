import time
import cv2
import pyautogui
import pygetwindow
import pyscreeze
from PIL import ImageGrab
window = pygetwindow.getWindowsWithTitle("Clash of Clans")[0]
screenshot = pyautogui.screenshot(region=(300, 200, 1200, 550))
coordinates = pyscreeze.locate(needleImage="AIR_DEFENSE_LEVEL_9.png", haystackImage=screenshot, grayscale=True, confidence=.5)


time.sleep(2)
pyautogui.click(coordinates)

