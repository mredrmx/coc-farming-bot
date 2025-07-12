import random
import time
import threading
from screen_utils import click

# --------------------------------------------- TR --------------------------------------------- #
# Adından anlaşıldığı gibi: Trophy düşürme işlemi (eşleşme bul, Zap kullan, pes et, tekrarla)
# "Counter" değerine ulaşana kadar çalışır
# 
# İşlem adımları:
# 1. Eşleşme ara
# 2. Zap büyüsü kullan
# 3. Saldırıdan vazgeç
# 4. Tekrarla
# 
# Amaç: Düşük trophy seviyesinde daha kolay yağma bulmak

# --------------------------------------------- ENG --------------------------------------------- #
# Does what the name says: Trophies derank (find match, zap, give up, repeat;
# Runs until "Counter" is reached

class TrophyDeranker:
    def __init__(self):
        # Performans parametreleri
        self.search_wait_time = 8  # Eşleşme bekleme süresi
        self.zap_wait_time = (1, 2)  # Zap sonrası bekleme aralığı
        self.surrender_wait_time = (0.3, 0.8)  # Pes etme bekleme aralığı
        self.confirm_wait_time = (0.4, 0.7)  # Onay bekleme aralığı
        self.menu_wait_time = 1.5  # Ana menü dönüş bekleme süresi
        self.click_delay = 0.5  # Tıklama arası bekleme
        
        # Thread güvenliği
        self._lock = threading.Lock()
        self._running = False
        self._counter = 0
        
    def start_deranking(self, max_attacks=30):
        """Trophy düşürme işlemini başlatır"""
        with self._lock:
            if self._running:
                print("Trophy deranker zaten çalışıyor!")
                return False
            self._running = True
            self._counter = 0
            
        print(f"Trophy deranker başlatıldı - {max_attacks} saldırı hedefi")
        
        # Başlangıç bekleme süresi
        time.sleep(5)
        
        try:
            while self._counter < max_attacks and self._running:
                self._perform_derank_cycle()
                self._counter += 1
                
        except KeyboardInterrupt:
            print("Trophy deranker kullanıcı tarafından durduruldu")
        finally:
            with self._lock:
                self._running = False
            print(f"Trophy deranker tamamlandı - {self._counter} saldırı yapıldı")
    
    def stop_deranking(self):
        """Trophy düşürme işlemini durdurur"""
        with self._lock:
            self._running = False
        print("Trophy deranker durduruldu")
    
    def is_running(self):
        """Botun çalışıp çalışmadığını kontrol eder"""
        with self._lock:
            return self._running
    
    def get_progress(self):
        """Mevcut ilerlemeyi döndürür"""
        with self._lock:
            return self._counter
    
    def _perform_derank_cycle(self):
        """Tek bir trophy düşürme döngüsünü gerçekleştirir"""
        if not self._running:
            return
            
        time.sleep(1)
        
        # Eşleşme arama ekranına geç
        click(100, 1000)  # Arama butonuna tıkla
        time.sleep(self.click_delay)
        click(1400, 700)  # Onay butonuna tıkla
        time.sleep(self.search_wait_time)  # Eşleşme için bekle
        
        if not self._running:
            return
            
        # Zap büyüsü kullan
        click(1350, 1000)  # Zap büyüsü butonuna tıkla
        # Rastgele konuma Zap bırak
        click(960 + random.randint(-150, 150), 540 + random.randint(-150, 150))
        time.sleep(random.randint(*self.zap_wait_time))
        
        if not self._running:
            return
            
        # Saldırıdan vazgeç
        click(150, 850)  # Pes et butonuna tıkla
        time.sleep(random.uniform(*self.surrender_wait_time))
        click(1170, 700)  # Onay butonuna tıkla
        time.sleep(random.uniform(*self.confirm_wait_time))
        click(960, 930)   # Ana menüye dön butonuna tıkla
        time.sleep(self.menu_wait_time)

# Global instance
deranker = TrophyDeranker()

# Eski uyumluluk için basit fonksiyon
def start_trophy_deranking(max_attacks=30):
    """Eski uyumluluk için basit trophy düşürme fonksiyonu"""
    deranker.start_deranking(max_attacks)

if __name__ == "__main__":
    # Test için
    start_trophy_deranking(5)
