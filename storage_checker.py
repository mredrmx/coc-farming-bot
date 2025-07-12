import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import time
import threading
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
        
        # Performans iyileştirmeleri
        self._last_check_time = 0
        self._check_cooldown = 5  # 5 saniye bekleme süresi
        self._cached_result = None
        self._cache_duration = 30  # 30 saniye cache süresi
        
        # Thread güvenliği
        self._lock = threading.Lock()
        
        # Tesseract ayarları
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        
        # Dosya temizliği için geçici dosyalar listesi
        self._temp_files = set()
        
    def check_storage_fullness(self) -> tuple[bool, float]:
        """
        Depo doluluk oranını kontrol eder
        Returns:
            tuple[bool, float]: (is_full, fullness_percentage) - is_full True if storage is full (>= 90%), fullness_percentage is the current percentage
        """
        with self._lock:
            current_time = time.time()
            
            # Cache kontrolü
            if (self._cached_result and 
                current_time - self._last_check_time < self._cache_duration):
                logger.debug("Depo durumu cache'den alındı")
                return self._cached_result
            
            # Cooldown kontrolü
            if current_time - self._last_check_time < self._check_cooldown:
                logger.debug("Depo kontrolü cooldown süresinde")
                return False, 0.0
        
        try:
            # Depo kontrolü için ayrı dosya kullan
            storage_path = f"storage_screenshot_{int(time.time())}.png"
            self._temp_files.add(storage_path)
            
            # Depo bölgesinin ekran görüntüsünü al (1660, 20, 260, 180)
            screenshot(storage_path, region=(1660, 20, 260, 180))
            
            # Görüntüyü yükle
            cv2_image = cv2.imread(storage_path)
            if cv2_image is None:
                logger.error("Depo ekran görüntüsü yüklenemedi!")
                self._cleanup_file(storage_path)
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
                self._cleanup_file(storage_path)
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
                
                # Sonucu cache'le
                with self._lock:
                    self._cached_result = (is_full, fullness_percentage)
                    self._last_check_time = current_time
                
                # Temizlik yap
                self._cleanup_file(storage_path)
                
                return is_full, fullness_percentage
                
            except ValueError as e:
                logger.error(f"Depo değerleri parse edilemedi: {lines}, Hata: {e}")
                self._cleanup_file(storage_path)
                return False, 0.0
                    
        except Exception as e:
            logger.error(f"Depo kontrolü sırasında hata: {e}")
            # Hata durumunda da temizlik yap
            self._cleanup_file(storage_path)
            return False, 0.0
    
    def should_check_storage(self) -> bool:
        """
        Depo kontrolü yapılması gerekip gerekmediğini kontrol eder
        Returns:
            bool: True if storage should be checked
        """
        with self._lock:
            self.attack_counter += 1
            return self.attack_counter % self.check_interval == 0
    
    def reset_counter(self):
        """Sayaç sıfırlama (test için)"""
        with self._lock:
            self.attack_counter = 0
    
    def get_current_count(self) -> int:
        """Mevcut saldırı sayısını döndürür"""
        with self._lock:
            return self.attack_counter
    
    def clear_cache(self):
        """Cache'i temizler"""
        with self._lock:
            self._cached_result = None
            self._last_check_time = 0
    
    def set_check_interval(self, interval: int):
        """Kontrol aralığını ayarlar"""
        with self._lock:
            self.check_interval = max(1, interval)
    
    def set_cache_duration(self, duration: int):
        """Cache süresini ayarlar"""
        with self._lock:
            self._cache_duration = max(1, duration)
    
    def _cleanup_file(self, file_path: str):
        """Belirli bir dosyayı temizler"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self._temp_files.discard(file_path)
                logger.debug(f"Dosya temizlendi: {file_path}")
        except Exception as e:
            logger.warning(f"Dosya temizleme hatası: {e}")
    
    def cleanup_all_temp_files(self):
        """Tüm geçici dosyaları temizler"""
        with self._lock:
            files_to_remove = list(self._temp_files)
        
        for file_path in files_to_remove:
            self._cleanup_file(file_path)
        
        logger.info("Tüm geçici dosyalar temizlendi")
    
    def __del__(self):
        """Destructor - temizlik yapar"""
        self.cleanup_all_temp_files()

# Global instance
storage_checker = StorageChecker() 