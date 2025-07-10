import time
from used_account import get_account_choice
from base_search import searchforbase
from screen_utils import print_screen_info

# --------------------------------------------- TR --------------------------------------------- #
# Ana program mantığı. Burada hesap seçimi sorgulanır ve "searchforbase" fonksiyonuna aktarılır. 
# Sonrasında yağma süreci kod durdurulana kadar çalışır. (Henüz geliştirilebilir durumda.)
# 
# Program akışı:
# 1. Kullanıcıdan hesap seçimi alınır (1 veya 2)
# 2. Sürekli döngüde base arama işlemi yapılır
# 3. Her 5 saniyede bir yeni base aranır

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic. Here the account choice is queried and passed to "searchforbase". Then the loot process runs
# until the code is stopped. (Still expandable.)

# Kullanıcıdan hesap seçimini al
used_account = get_account_choice()

# Ekran bilgilerini göster
print_screen_info()

# Ana döngü - sürekli base arama ve saldırı
while True:
    time.sleep(5)  # 5 saniye bekle
    searchforbase(used_account)  # Base ara ve uygun bulursa saldır