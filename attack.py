import random
import time
import threading
from attacks_by_position import e_drags_top_left, e_drags_top_right, e_drags_bottom_left, \
    e_drags_bottom_right, dragons_top_right, dragons_top_left, dragons_bottom_right, \
    dragons_bottom_left
from screen_utils import click

# --------------------------------------------- TR --------------------------------------------- #
# Base bulunduğunda saldırıların arkasındaki ana mantık.
# "attack_positions" listesinden rastgele bir saldırı pozisyonu seçilir ve, pozisyona ve hesaba bağlı olarak saldırılır.
# Saldırılar, düzen için "AttacksByPosition" dosyasından import edilir (çok fazla manuel iş/deneme yanılma)
# 
# Saldırı türleri:
# - Account 1: E-Dragon saldırısı (daha güçlü hesap)
# - Account 2: Dragon saldırısı (daha zayıf hesap)

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic behind the attacks, if a base has been found.
# A random attack position is selected from "attack_positions" and, depending on the position and account, attacked.
# The attacks are imported from "AttacksByPosition" for the sake of clarity (a lot of annoying
# manual work/trial and error)

class AttackManager:
    def __init__(self):
        # Performans parametreleri
        self.e_drag_click_delay = 0.3  # E-Dragon tıklama arası bekleme
        self.dragon_click_delay = 1.0  # Dragon tıklama arası bekleme
        self.menu_return_wait = 2  # Ana menü dönüş bekleme süresi
        
        # Saldırı pozisyonları
        self.attack_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]
        
        # Thread güvenliği
        self._lock = threading.Lock()
        self._attack_counter = 0
        self._last_attack_time = 0
        self._attack_cooldown = 3  # 3 saniye saldırı arası bekleme
        
        # Saldırı istatistikleri
        self._attack_stats = {
            "e_dragons": 0,
            "dragons": 0,
            "total_attacks": 0
        }
    
    def attack_with_e_drags(self):
        """E-Dragon saldırısı gerçekleştirir"""
        with self._lock:
            if time.time() - self._last_attack_time < self._attack_cooldown:
                print("Saldırı cooldown süresinde, bekleniyor...")
                return False
            self._last_attack_time = time.time()
            self._attack_counter += 1
            self._attack_stats["e_dragons"] += 1
            self._attack_stats["total_attacks"] += 1
        
        try:
            # Rastgele başlangıç pozisyonu seç
            start_position = random.choice(self.attack_positions)
            print(f"E-Dragon saldırısı başlatıldı - Pozisyon: {start_position}")
            
            # Seçilen pozisyona göre saldırı stratejisini uygula
            if start_position == "top_left":
                e_drags_top_left()
            elif start_position == "top_right":
                e_drags_top_right()
            elif start_position == "bottom_left":
                e_drags_bottom_left()
            elif start_position == "bottom_right":
                e_drags_bottom_right()
            
            # Saldırı sonrası işlemler
            self._post_attack_cleanup(self.e_drag_click_delay)
            print("E-Dragon saldırısı tamamlandı.")
            return True
            
        except Exception as e:
            print(f"E-Dragon saldırısı hatası: {e}")
            return False
    
    def attack_with_dragons(self):
        """Dragon saldırısı gerçekleştirir"""
        with self._lock:
            if time.time() - self._last_attack_time < self._attack_cooldown:
                print("Saldırı cooldown süresinde, bekleniyor...")
                return False
            self._last_attack_time = time.time()
            self._attack_counter += 1
            self._attack_stats["dragons"] += 1
            self._attack_stats["total_attacks"] += 1
        
        try:
            # Rastgele başlangıç pozisyonu seç
            start_position = random.choice(self.attack_positions)
            print(f"Dragon saldırısı başlatıldı - Pozisyon: {start_position}")
            
            # Seçilen pozisyona göre saldırı stratejisini uygula
            if start_position == "top_left":
                dragons_top_left()
            elif start_position == "top_right":
                dragons_top_right()
            elif start_position == "bottom_left":
                dragons_bottom_left()
            elif start_position == "bottom_right":
                dragons_bottom_right()
            
            # Saldırı sonrası işlemler
            self._post_attack_cleanup(self.dragon_click_delay)
            print("Dragon saldırısı tamamlandı.")
            return True
            
        except Exception as e:
            print(f"Dragon saldırısı hatası: {e}")
            return False
    
    def _post_attack_cleanup(self, click_delay):
        """Saldırı sonrası temizlik işlemleri"""
        click(150, 850)  # Saldırı sonu butonuna tıkla
        time.sleep(click_delay)
        click(1170, 700)  # Onay butonuna tıkla
        time.sleep(click_delay)
        click(960, 930)   # Ana menüye dön butonuna tıkla
        time.sleep(self.menu_return_wait)
    
    def get_attack_count(self):
        """Toplam saldırı sayısını döndürür"""
        with self._lock:
            return self._attack_counter
    
    def get_attack_stats(self):
        """Saldırı istatistiklerini döndürür"""
        with self._lock:
            return self._attack_stats.copy()
    
    def reset_stats(self):
        """İstatistikleri sıfırlar"""
        with self._lock:
            self._attack_counter = 0
            self._attack_stats = {
                "e_dragons": 0,
                "dragons": 0,
                "total_attacks": 0
            }
    
    def set_attack_cooldown(self, cooldown):
        """Saldırı arası bekleme süresini ayarlar"""
        with self._lock:
            self._attack_cooldown = max(0, cooldown)
    
    def set_e_drag_click_delay(self, delay):
        """E-Dragon tıklama gecikmesini ayarlar"""
        self.e_drag_click_delay = max(0.1, delay)
    
    def set_dragon_click_delay(self, delay):
        """Dragon tıklama gecikmesini ayarlar"""
        self.dragon_click_delay = max(0.1, delay)
    
    def set_menu_return_wait(self, wait_time):
        """Ana menü dönüş bekleme süresini ayarlar"""
        self.menu_return_wait = max(0.5, wait_time)

# Global instance
attack_manager = AttackManager()

# Eski uyumluluk için fonksiyonlar
def attack_with_e_drags():
    """Eski uyumluluk için E-Dragon saldırısı fonksiyonu"""
    return attack_manager.attack_with_e_drags()

def attack_with_dragons():
    """Eski uyumluluk için Dragon saldırısı fonksiyonu"""
    return attack_manager.attack_with_dragons()

# Eski uyumluluk için değişkenler
attack_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]
