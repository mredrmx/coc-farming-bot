import random
import time
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

# Sayaç ve başlangıç bekleme süresi
counter = 0
time.sleep(5)  # Başlangıç için 5 saniye bekle

# Trophy düşürme döngüsü
while counter < 30:  # 30 kez tekrarla
    time.sleep(1)
    
    # Eşleşme arama ekranına geç
    click(100, 1000)  # Arama butonuna tıkla
    time.sleep(0.5)
    click(1400, 700)  # Onay butonuna tıkla
    time.sleep(8)  # Eşleşme için bekle
    
    # Zap büyüsü kullan
    click(1350, 1000)  # Zap büyüsü butonuna tıkla
    # Rastgele konuma Zap bırak
    click(960 + random.randint(-150, 150), 540 + random.randint(-150, 150))
    time.sleep(random.randint(1, 2))
    
    # Saldırıdan vazgeç
    click(150, 850)  # Pes et butonuna tıkla
    time.sleep(random.uniform(0.3, 0.8))
    click(1170, 700)  # Onay butonuna tıkla
    time.sleep(random.uniform(0.4, 0.7))
    click(960, 930)   # Ana menüye dön butonuna tıkla
    time.sleep(1.5)
    
    counter += 1  # Sayacı artır
