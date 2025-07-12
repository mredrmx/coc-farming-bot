import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
import threading
import os
from attack import attack_with_e_drags, attack_with_dragons
from dotenv import load_dotenv
from screen_utils import click, screenshot, print_screen_info

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

class BaseSearcher:
    def __init__(self):
        # Performans parametreleri
        self.search_wait_time = 10  # Base arama bekleme süresi
        self.next_base_wait_time = 10  # Sonraki base bekleme süresi
        self.click_delay = 0.5  # Tıklama arası bekleme
        self.ocr_wait_time = 2  # OCR işlemi bekleme süresi
        self.retry_wait_time = 10  # Hata durumunda bekleme süresi
        
        # Yağma limitleri
        self.MIN_COMBINED_MAIN_ACCOUNT = 1800000  # Ana hesap için minimum toplam yağma (1.8 Milyon Elixir + Altın)
        self.MIN_COMBINED_ALT_ACCOUNT = 1200000   # İkinci hesap için minimum toplam yağma (1.2 Milyon Elixir + Altın)
        self.MAX_GOLD_MAIN = 2500000  # Ana hesap maksimum altın
        self.MAX_ELIXIR_MAIN = 2500000  # Ana hesap maksimum elixir
        self.MAX_GOLD_ALT = 1400000  # Alt hesap maksimum altın
        self.MAX_ELIXIR_ALT = 1400000  # Alt hesap maksimum elixir
        
        # Thread güvenliği
        self._lock = threading.Lock()
        self._looking_for_base = True
        self._attack_counter = 0
        
        # Dosya temizliği
        self._temp_files = set()
        
        # Çevre değişkenlerini yükle
        load_dotenv()
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
    
    def search_for_base(self, user_account):
        """Base arama işlemini başlatır"""
        with self._lock:
            self._looking_for_base = True
        
        print(f"Base arama başlatıldı - Hesap: {user_account}")
        time.sleep(1)
        
        # Ekran bilgilerini göster
        print_screen_info()
        
        # Base arama ekranına geç
        click(100, 1000)  # Arama butonuna tıkla
        time.sleep(self.click_delay)
        click(1400, 700)  # Onay butonuna tıkla
        time.sleep(self.search_wait_time)  # Arama için bekle
        
        # Base arama döngüsü
        while self._looking_for_base:
            try:
                if not self._perform_base_check(user_account):
                    # Sonraki base'ye geç
                    click(x=1785, y=820)  # Sonraki base butonuna tıkla
                    time.sleep(self.next_base_wait_time)
                else:
                    # Uygun base bulundu, saldırı başlat
                    break
                    
            except Exception as e:
                print(f"Base arama hatası: {e}")
                print(f"{self.retry_wait_time} saniye bekleyip tekrar deneyeceğim...")
                time.sleep(self.retry_wait_time)
        
        # Döngü sonunda durumu sıfırla
        with self._lock:
            self._looking_for_base = True
    
    def _perform_base_check(self, user_account):
        """Tek bir base kontrolü yapar"""
        path = os.getenv("SCREENSHOT_PATH")
        if path is None:
            print("Hata: Screenshot yolu bulunamadı!")
            return False
        
        # Geçici dosya adı oluştur
        temp_path = f"base_search_{int(time.time())}.png"
        self._temp_files.add(temp_path)
        
        try:
            # Yağma miktarını gösteren alanın ekran görüntüsünü al
            screenshot(temp_path, region=(30, 120, 250, 130))
            
            # Ekran görüntüsünü yükle ve işle
            cv2_image = cv2.imread(temp_path)
            if cv2_image is None:
                print("Hata: Ekran görüntüsü yüklenemedi!")
                return False
                
            # Görüntü işleme
            hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
            
            # Beyaz renk aralığını tanımla (yağma metni için)
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 60, 255])
            mask = cv2.inRange(hsv, lower_white, upper_white)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

            # Maskeyi pytesseract için PIL-Image'e dönüştür
            mask_pil = Image.fromarray(mask)

            time.sleep(self.ocr_wait_time)

            # İşlenmiş görüntüye OCR uygula
            result = pytesseract.image_to_string(mask_pil, timeout=2, lang='eng',
                                                 config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789')
            result = result.replace('\n\n', '\n')
            loot_list = result.splitlines()
            
            # Hesap tipine göre kontrol
            if user_account == "1":
                return self._check_main_account_loot(loot_list)
            elif user_account == "2":
                return self._check_alt_account_loot(loot_list)
            else:
                print(f"Bilinmeyen hesap tipi: {user_account}")
                return False
                
        except Exception as e:
            print(f"Base kontrolü hatası: {e}")
            return False
        finally:
            # Geçici dosyayı temizle
            self._cleanup_file(temp_path)
    
    def _check_main_account_loot(self, loot_list):
        """Ana hesap için yağma kontrolü"""
        try:
            gold = int(loot_list[0])
            elixir = int(loot_list[1])
            total = gold + elixir
            
            if (self.MIN_COMBINED_MAIN_ACCOUNT <= total and 
                gold < self.MAX_GOLD_MAIN and 
                elixir < self.MAX_ELIXIR_MAIN):
                print(f"Found good base! Gold: {gold:,}, Elixir: {elixir:,}, Total: {total:,}")
                self._looking_for_base = False
                attack_with_e_drags()  # E-Dragon saldırısı başlat
                return True
            return False
        except (ValueError, IndexError):
            return False
    
    def _check_alt_account_loot(self, loot_list):
        """Alt hesap için yağma kontrolü"""
        try:
            gold = int(loot_list[0])
            elixir = int(loot_list[1])
            total = gold + elixir
            
            if (self.MIN_COMBINED_ALT_ACCOUNT <= total and 
                gold < self.MAX_GOLD_ALT and 
                elixir < self.MAX_ELIXIR_ALT):
                print(f"Found good base! Gold: {gold:,}, Elixir: {elixir:,}, Total: {total:,}")
                self._looking_for_base = False
                attack_with_dragons()  # Dragon saldırısı başlat
                return True
            return False
        except (ValueError, IndexError):
            return False
    
    def stop_search(self):
        """Base aramayı durdurur"""
        with self._lock:
            self._looking_for_base = False
    
    def is_searching(self):
        """Base arama durumunu kontrol eder"""
        with self._lock:
            return self._looking_for_base
    
    def get_attack_count(self):
        """Saldırı sayısını döndürür"""
        with self._lock:
            return self._attack_counter
    
    def set_search_wait_time(self, wait_time):
        """Arama bekleme süresini ayarlar"""
        self.search_wait_time = max(1, wait_time)
    
    def set_next_base_wait_time(self, wait_time):
        """Sonraki base bekleme süresini ayarlar"""
        self.next_base_wait_time = max(1, wait_time)
    
    def _cleanup_file(self, file_path):
        """Geçici dosyayı temizler"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self._temp_files.discard(file_path)
        except Exception as e:
            print(f"Dosya temizleme hatası: {e}")
    
    def cleanup_all_temp_files(self):
        """Tüm geçici dosyaları temizler"""
        with self._lock:
            files_to_remove = list(self._temp_files)
        
        for file_path in files_to_remove:
            self._cleanup_file(file_path)
        
        print("Tüm geçici dosyalar temizlendi")
    
    def __del__(self):
        """Destructor - temizlik yapar"""
        self.cleanup_all_temp_files()

# Global instance
base_searcher = BaseSearcher()

# Eski uyumluluk için fonksiyon
def searchforbase(user_account):
    """Eski uyumluluk için base arama fonksiyonu"""
    base_searcher.search_for_base(user_account)

# Global değişkenler (eski uyumluluk için)
LOOKING_FOR_BASE = True
MIN_COMBINED_MAIN_ACCOUNT = 1800000
MIN_COMBINED_ALT_ACCOUNT = 1200000
ATTACK_COUNTER = 0
