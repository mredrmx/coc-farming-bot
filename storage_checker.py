import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
from screen_utils import screenshot
from dotenv import load_dotenv
import logging

# Çevre değişkenlerini yükle
load_dotenv()

# Logging ayarları
logger = logging.getLogger(__name__)

class StorageChecker:
    def __init__(self):
        self.storage_capacity = 36000000  # 36 milyon ganimet kapasitesi
        self.check_interval = 10  # Her 10 saldırıda bir kontrol
        self.attack_counter = 0
        
        # Tesseract ayarları
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        
    def check_storage_fullness(self) -> tuple[bool, float]:
        """
        Depo doluluk oranını kontrol eder
        Returns:
            tuple[bool, float]: (is_full, fullness_percentage) - is_full True if storage is full (>= 90%), fullness_percentage is the current percentage
        """
        try:
            # Depo kontrolü için ayrı dosya kullan
            storage_path = "storage_screenshot.png"
            
            # Depo bölgesinin ekran görüntüsünü al (1660, 20, 260, 180)
            screenshot(storage_path, region=(1660, 20, 260, 180))
            
            # Görüntüyü yükle
            cv2_image = cv2.imread(storage_path)
            if cv2_image is None:
                logger.error("Depo ekran görüntüsü yüklenemedi!")
                return False, 0.0
            
            # Görüntüyü işle
            hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
            
            # Beyaz renk aralığını tanımla (depo metni için)
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 60, 255])
            mask = cv2.inRange(hsv, lower_white, upper_white)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            
            # Maskeyi PIL Image'e dönüştür
            mask_pil = Image.fromarray(mask)
            
            # OCR uygula - Sadece sayıları oku
            result = pytesseract.image_to_string(
                mask_pil, 
                timeout=2, 
                lang='eng',
                config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789'
            )
            
            # Sonucu temizle ve satırlara böl
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            
            if len(lines) < 2:
                logger.warning(f"Yeterli depo bilgisi okunamadı. Satır sayısı: {len(lines)}")
                self.cleanup_screenshot()
                return False, 0.0
            
            try:
                # İlk iki deponun değerlerini al (Altın + Elixir)
                gold_amount = int(lines[0]) if lines[0].isdigit() else 0
                elixir_amount = int(lines[1]) if lines[1].isdigit() else 0
                
                # Toplam depo değeri (sadece Altın + Elixir)
                total_current = gold_amount + elixir_amount
                
                # Doluluk oranını hesapla (18M kapasite)
                fullness_percentage = (total_current / self.storage_capacity) * 100
                
                logger.info(f"Depo durumu: Altın {gold_amount:,} + Elixir {elixir_amount:,} = {total_current:,}/{self.storage_capacity:,} ({fullness_percentage:.1f}%)")
                
                is_full = fullness_percentage >= 90
                
                # Temizlik yap
                self.cleanup_screenshot()
                
                return is_full, fullness_percentage
                
            except ValueError as e:
                logger.error(f"Depo değerleri parse edilemedi: {lines}, Hata: {e}")
                self.cleanup_screenshot()
                return False, 0.0
                    
        except Exception as e:
            logger.error(f"Depo kontrolü sırasında hata: {e}")
            # Hata durumunda da temizlik yap
            self.cleanup_screenshot()
            return False, 0.0
    
    def should_check_storage(self) -> bool:
        """
        Depo kontrolü yapılması gerekip gerekmediğini kontrol eder
        Returns:
            bool: True if storage should be checked
        """
        self.attack_counter += 1
        return self.attack_counter % self.check_interval == 0
    
    def reset_counter(self):
        """Sayaç sıfırlama (test için)"""
        self.attack_counter = 0
    
    def get_current_count(self) -> int:
        """Mevcut saldırı sayısını döndürür"""
        return self.attack_counter
    
    def cleanup_screenshot(self):
        """Geçici screenshot dosyasını temizler"""
        try:
            storage_path = "storage_screenshot.png"
            if os.path.exists(storage_path):
                os.remove(storage_path)
                logger.debug("Depo screenshot dosyası temizlendi")
        except Exception as e:
            logger.warning(f"Screenshot temizleme hatası: {e}")

# Global instance
storage_checker = StorageChecker() 