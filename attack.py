import random
import time
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

# Rastgele saldırı pozisyonları
attack_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]


# "Saint" hesabı için E-Dragon saldırısı
def attack_with_e_drags():
    # Rastgele başlangıç pozisyonu seç
    start_position = random.choice(attack_positions)
    
    # Seçilen pozisyona göre saldırı stratejisini uygula
    if start_position == "top_left":
        e_drags_top_left()
    elif start_position == "top_right":
        e_drags_top_left()
    elif start_position == "bottom_left":
        e_drags_bottom_left()
    elif start_position == "bottom_right":
        e_drags_bottom_right()
    
    # Saldırı sonrası işlemler
    print("Saldırı tamamlandı.")
    click(150, 850)  # Saldırı sonu butonuna tıkla
    time.sleep(0.3)
    click(1170, 700)  # Onay butonuna tıkla
    time.sleep(0.3)
    click(960, 930)   # Ana menüye dön butonuna tıkla
    time.sleep(2)


# "Hero" hesabı için Dragon saldırısı
def attack_with_dragons():
    # Rastgele başlangıç pozisyonu seç
    start_position = random.choice(attack_positions)
    
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
    print("Saldırı tamamlandı.")
    click(150, 850)  # Saldırı sonu butonuna tıkla
    time.sleep(1)
    click(1170, 700)  # Onay butonuna tıkla
    time.sleep(1)
    click(960, 930)   # Ana menüye dön butonuna tıkla
    time.sleep(2)
