#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash of Clans Bot - Ekran Seçimi
Clash of Clans Bot - Screen Selection
"""

import pyautogui
import tkinter as tk
from tkinter import ttk
import json
import os

class ScreenSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clash of Clans Bot - Ekran Seçimi")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Ekran bilgilerini al
        self.screens = self.get_screen_info()
        self.selected_screen = None
        
        self.setup_ui()
        
    def get_screen_info(self):
        """Mevcut ekranları tespit et"""
        screens = []
        
        # Ana ekran
        primary_width, primary_height = pyautogui.size()
        screens.append({
            'name': 'Ana Ekran (Primary)',
            'width': primary_width,
            'height': primary_height,
            'offset_x': 0,
            'offset_y': 0
        })
        
        # Yaygın ikinci ekran boyutları (manuel seçim için)
        common_screens = [
            {'name': 'İkinci Ekran (1920x1080)', 'width': 1920, 'height': 1080, 'offset_x': 1920, 'offset_y': 0},
            {'name': 'İkinci Ekran (1366x768)', 'width': 1366, 'height': 768, 'offset_x': 1920, 'offset_y': 0},
            {'name': 'İkinci Ekran (2560x1440)', 'width': 2560, 'height': 1440, 'offset_x': 1920, 'offset_y': 0},
            {'name': 'İkinci Ekran (3840x2160)', 'width': 3840, 'height': 2160, 'offset_x': 1920, 'offset_y': 0},
        ]
        
        screens.extend(common_screens)
        return screens
    
    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Başlık
        title_label = tk.Label(self.root, text="Clash of Clans Bot - Ekran Seçimi", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Açıklama
        desc_label = tk.Label(self.root, text="Clash of Clans'ın çalıştığı ekranı seçin:", 
                             font=("Arial", 12))
        desc_label.pack(pady=10)
        
        # Ekran listesi
        self.screen_var = tk.StringVar()
        screen_frame = tk.Frame(self.root)
        screen_frame.pack(pady=20)
        
        for i, screen in enumerate(self.screens):
            radio = tk.Radiobutton(screen_frame, 
                                 text=f"{screen['name']} ({screen['width']}x{screen['height']})",
                                 variable=self.screen_var, 
                                 value=str(i),
                                 font=("Arial", 11))
            radio.pack(anchor='w', pady=5)
        
        # Varsayılan olarak ilk ekranı seç
        if self.screens:
            self.screen_var.set("0")
        
        # Butonlar
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=30)
        
        test_btn = tk.Button(button_frame, text="Ekranı Test Et", 
                           command=self.test_screen, 
                           bg="#4CAF50", fg="white", font=("Arial", 12))
        test_btn.pack(side=tk.LEFT, padx=10)
        
        save_btn = tk.Button(button_frame, text="Kaydet ve Çık", 
                           command=self.save_and_exit, 
                           bg="#2196F3", fg="white", font=("Arial", 12))
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="İptal", 
                             command=self.root.quit, 
                             bg="#f44336", fg="white", font=("Arial", 12))
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Durum etiketi
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)
    
    def test_screen(self):
        """Seçili ekranı test et"""
        try:
            screen_index = int(self.screen_var.get())
            screen = self.screens[screen_index]
            
            self.status_label.config(text=f"Test ediliyor: {screen['name']}...")
            self.root.update()
            
            # Test için ekranın ortasına tıkla
            center_x = screen['offset_x'] + screen['width'] // 2
            center_y = screen['offset_y'] + screen['height'] // 2
            
            # Fareyi o ekrana taşı
            pyautogui.moveTo(center_x, center_y, duration=1)
            
            self.status_label.config(text=f"✅ Test başarılı! Fare {screen['name']} ekranına taşındı.")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Test başarısız: {str(e)}")
    
    def save_and_exit(self):
        """Seçimi kaydet ve çık"""
        try:
            screen_index = int(self.screen_var.get())
            screen = self.screens[screen_index]
            
            # Ekran ayarlarını kaydet
            config = {
                'screen_offset_x': screen['offset_x'],
                'screen_offset_y': screen['offset_y'],
                'screen_width': screen['width'],
                'screen_height': screen['height'],
                'screen_name': screen['name']
            }
            
            with open('screen_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.status_label.config(text=f"✅ Ayarlar kaydedildi: {screen['name']}")
            self.root.after(2000, self.root.quit)  # 2 saniye sonra kapat
            
        except Exception as e:
            self.status_label.config(text=f"❌ Kaydetme hatası: {str(e)}")
    
    def run(self):
        """Arayüzü başlat"""
        self.root.mainloop()

def main():
    """Ana fonksiyon"""
    print("🎮 Clash of Clans Bot - Ekran Seçimi")
    print("=" * 50)
    
    # Ana ekran bilgilerini göster
    primary_width, primary_height = pyautogui.size()
    print(f"Ana ekran: {primary_width}x{primary_height}")
    print("İkinci ekran seçenekleri arayüzde gösterilecek...")
    
    print("\nEkran seçimi arayüzü açılıyor...")
    
    # Arayüzü başlat
    app = ScreenSelector()
    app.run()
    
    # Kaydedilen ayarları kontrol et
    if os.path.exists('screen_config.json'):
        with open('screen_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"\n✅ Ekran ayarları kaydedildi: {config['screen_name']}")
        print(f"   Offset: ({config['screen_offset_x']}, {config['screen_offset_y']})")
        print(f"   Boyut: {config['screen_width']}x{config['screen_height']}")
    else:
        print("\n❌ Ekran ayarları kaydedilmedi!")

if __name__ == "__main__":
    main() 