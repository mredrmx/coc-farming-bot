
# --------------------------------------------- TR --------------------------------------------- #
# Kullanıcıdan hesap seçimi (1/2) için giriş ister. Geçersiz giriş durumunda tekrar sorar.
# 
# Fonksiyon amacı:
# - Kullanıcıdan 1 veya 2 değerini alır
# - Geçersiz giriş durumunda uyarı verir ve tekrar sorar
# - Geçerli giriş durumunda seçimi döndürür

# --------------------------------------------- ENG --------------------------------------------- #
# Asks for input for account 1/2, if invalid then renewed query

def get_account_choice():
    # Kullanıcıdan giriş al ve boşlukları temizle
    choice = input("Hesap seçimi (1 veya 2): ").strip()
    
    # Girişin geçerli olup olmadığını kontrol et
    if choice not in ["1", "2"]:
        print("Geçersiz giriş! Lütfen 1 veya 2 girin.")
        return get_account_choice()  # Tekrar sor
    
    return choice  # Geçerli seçimi döndür
