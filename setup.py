#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash of Clans Bot - Kurulum Scripti
Clash of Clans Bot - Setup Script
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Python sürümünü kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        print(f"Mevcut sürüm: {sys.version}")
        return False
    print(f"✅ Python sürümü uygun: {sys.version}")
    return True

def install_requirements():
    """Gerekli Python kütüphanelerini kur"""
    print("\n📦 Python kütüphaneleri kuruluyor...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python kütüphaneleri başarıyla kuruldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Kütüphane kurulumu başarısız: {e}")
        return False

def check_tesseract():
    """Tesseract-OCR'ın kurulu olup olmadığını kontrol et"""
    print("\n🔍 Tesseract-OCR kontrol ediliyor...")
    
    # Yaygın kurulum yolları
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME'))
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract-OCR bulundu: {path}")
            return path
    
    print("❌ Tesseract-OCR bulunamadı!")
    print("📥 Lütfen şu adresten indirin: https://github.com/tesseract-ocr/tesseract/releases/")
    print("📁 C:\\Program Files\\Tesseract-OCR\\ klasörüne kurun")
    return None

def create_temp_directory():
    """Geçici klasör oluştur"""
    print("\n📁 Geçici klasör oluşturuluyor...")
    temp_dir = r"C:\temp"
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print(f"✅ Geçici klasör oluşturuldu: {temp_dir}")
        else:
            print(f"✅ Geçici klasör zaten mevcut: {temp_dir}")
        return True
    except Exception as e:
        print(f"❌ Geçici klasör oluşturulamadı: {e}")
        return False

def setup_env_file():
    """Çevre değişkenleri dosyasını ayarla"""
    print("\n⚙️ Çevre değişkenleri ayarlanıyor...")
    
    tesseract_path = check_tesseract()
    if not tesseract_path:
        print("⚠️ Tesseract-OCR bulunamadı, varsayılan yol kullanılacak")
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    env_content = f"""# Clash of Clans Bot - Çevre Değişkenleri
# Clash of Clans Bot - Environment Variables

# Tesseract-OCR dosya yolu (Tesseract-OCR file path)
TESSERACT_CMD={tesseract_path}

# Geçici ekran görüntüleri için dosya yolu (Temporary screenshot file path)
SCREENSHOT_PATH=C:\\temp\\screenshot.png
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env dosyası oluşturuldu!")
        return True
    except Exception as e:
        print(f"❌ .env dosyası oluşturulamadı: {e}")
        return False

def main():
    """Ana kurulum fonksiyonu"""
    print("🎮 Clash of Clans Bot - Kurulum Scripti")
    print("=" * 50)
    
    # Python sürüm kontrolü
    if not check_python_version():
        return False
    
    # Geçici klasör oluştur
    if not create_temp_directory():
        return False
    
    # Python kütüphanelerini kur
    if not install_requirements():
        return False
    
    # Çevre değişkenlerini ayarla
    if not setup_env_file():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Kurulum tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. Tesseract-OCR'ı kurun (eğer kurulu değilse)")
    print("2. Google Play Oyunları (Beta)'yı kurun")
    print("3. Clash of Clans'ı açın")
    print("4. main.py dosyasını çalıştırın")
    print("\n⚠️ Önemli: Bot'u yönetici olarak çalıştırın!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Kurulum başarısız! Lütfen hataları kontrol edin.")
        sys.exit(1)
    else:
        print("\n✅ Kurulum başarılı! Bot kullanıma hazır.") 