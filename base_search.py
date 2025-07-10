import time
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
from attack import attack_with_e_drags, attack_with_dragons
from dotenv import load_dotenv
import os

# --------------------------------------------- TR --------------------------------------------- #
# Belirli miktarda yağma içeren base arama fonksiyonunun arkasındaki ana mantık.
# OCR işlevi için pytesseract kullanır (yağma ekran görüntüsünden metin çıkarma)
# Ekran görüntüsü pyautogui ile alınır ve cv2 ile işlenir
# Sonrasında, hesaba bağlı olarak ("1" veya "2") "MIN_COMBINED_{ACCOUNT}" ile karşılaştırılır
# Yeterli yağma varsa -> Saldırı, aksi takdirde: Sonraki base
# 
# İşlem adımları:
# 1. Base arama ekranına geç
# 2. Yağma miktarını gösteren alanın ekran görüntüsünü al
# 3. Görüntüyü işle ve OCR ile metin çıkar
# 4. Yağma miktarını kontrol et ve karar ver

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic behind the search function for a base with a certain amount of loot.
# Uses pytesseract for the OCR function (text from screenshot of loot)
# Screenshot is taken by pyautogui and then processed with cv2
# Then, depending on the account ("1" or "2") is compared with the "MIN_COMBINED_{ACCOUNT}"
# If there is enough loot - > attack, otherwise: next base

# Global değişkenler
LOOKING_FOR_BASE = True  # Base arama durumu
MIN_COMBINED_MAIN_ACCOUNT = 1800000  # Ana hesap için minimum toplam yağma (1.8 Milyon Elixir + Altın)
MIN_COMBINED_ALT_ACCOUNT = 1200000   # İkinci hesap için minimum toplam yağma (1.2 Milyon Elixir + Altın)
ATTACK_COUNTER = 0  # Saldırı sayacı

# Çevre değişkenlerini yükle
load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")  # Tesseract-OCR dosya yolu
# Genellikle C:\Program Files\Tesseract-OCR veya C:\Program Files (x86)\Tesseract-OCR'da kurulu


def searchforbase(user_account):
    global LOOKING_FOR_BASE
    LOOKING_FOR_BASE = True  # ÇOK ÖNEMLİ: her başlangıçta True olarak ayarla!
    time.sleep(1)
    
    # Base arama ekranına geç
    pyautogui.click(100, 1000)  # Arama butonuna tıkla
    time.sleep(0.5)
    pyautogui.click(1400, 700)  # Onay butonuna tıkla
    time.sleep(5)  # Arama için bekle
    
    # Base arama döngüsü
    while LOOKING_FOR_BASE:
        path = os.getenv("SCREENSHOT_PATH")  # Geçici ekran görüntüleri için yol
        
        # Yağma miktarını gösteren alanın ekran görüntüsünü al
        pyautogui.screenshot(path, region=(30, 120, 250, 130))

        # Ekran görüntüsünü yükle ve işle (HSV + Maske)
        if path is None:
            print("Hata: Screenshot yolu bulunamadı!")
            continue
            
        cv2_image = cv2.imread(path)
        if cv2_image is None:
            print("Hata: Ekran görüntüsü yüklenemedi!")
            continue
            
        hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
        
        # Beyaz renk aralığını tanımla (yağma metni için)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 60, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Maskeyi pytesseract için PIL-Image'e dönüştür
        mask_pil = Image.fromarray(mask)

        time.sleep(2)

        # İşlenmiş görüntüye OCR uygula
        result = pytesseract.image_to_string(mask_pil, timeout=1, lang='eng',
                                             config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789')
        result = result.replace('\n\n', '\n')
        loot_list = result.splitlines()
        
        # Ana hesap (Account 1) için kontrol
        if user_account == "1":
            try:
                # Yağma miktarını kontrol et (minimum 1.8M toplam, maksimum 2.5M her biri)
                if MIN_COMBINED_MAIN_ACCOUNT <= int(loot_list[0]) + int(loot_list[1]) and int(loot_list[0]) < 2500000 and int(
                        loot_list[1]) < 2500000:
                    print(f"Found good base! Gold: {loot_list[0]}, Elixir: {loot_list[1]}")
                    LOOKING_FOR_BASE = False
                    attack_with_e_drags()  # E-Dragon saldırısı başlat
                    break  # ÇOK ÖNEMLİ: saldırıdan sonra döngüden çık!
                else:
                    pyautogui.click(x=1785, y=820)  # Sonraki base butonuna tıkla
                    time.sleep(5)
            except (ValueError, IndexError):
                # OCR hatası durumunda sonraki base'ye geç
                pyautogui.click(x=1785, y=820)
                time.sleep(5)

        # İkinci hesap (Account 2) için kontrol
        elif user_account == "2":
            try:
                # Yağma miktarını kontrol et (minimum 1.2M toplam, maksimum 1.4M her biri)
                if MIN_COMBINED_ALT_ACCOUNT <= int(loot_list[0]) + int(loot_list[1]) and int(loot_list[0]) < 1400000 and int(
                        loot_list[1]) < 1400000:
                    print(f"Found good base! Gold: {loot_list[0]}, Elixir: {loot_list[1]}")
                    LOOKING_FOR_BASE = False
                    attack_with_dragons()  # Dragon saldırısı başlat
                    break  # ÇOK ÖNEMLİ: saldırıdan sonra döngüden çık!
                else:
                    pyautogui.click(x=1785, y=820)  # Sonraki base butonuna tıkla
                    time.sleep(5)
            except (ValueError, IndexError):
                # OCR hatası durumunda sonraki base'ye geç
                pyautogui.click(x=1785, y=820)
                time.sleep(5)

    # Döngü sonunda durumu sıfırla
    LOOKING_FOR_BASE = True
