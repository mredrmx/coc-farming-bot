#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash of Clans Bot - Ekran Yardımcı Modülü
Clash of Clans Bot - Screen Utilities
"""

import json
import os
import pyautogui
import mss
import mss.tools

class ScreenManager:
    def __init__(self):
        self.config_file = 'screen_config.json'
        self.screen_config = self.load_config()
    
    def load_config(self):
        """Ekran konfigürasyonunu yükle"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Konfigürasyon yüklenemedi: {e}")
        
        # Varsayılan ayarlar (ana ekran)
        return {
            'screen_offset_x': 0,
            'screen_offset_y': 0,
            'screen_width': 1920,
            'screen_height': 1080,
            'screen_name': 'Ana Ekran (Varsayılan)'
        }
    
    def get_screen_offset(self):
        """Ekran offset'ini döndür"""
        return self.screen_config['screen_offset_x'], self.screen_config['screen_offset_y']
    
    def get_screen_size(self):
        """Ekran boyutunu döndür"""
        return self.screen_config['screen_width'], self.screen_config['screen_height']
    
    def adjust_coordinates(self, x, y):
        """Koordinatları seçili ekrana göre ayarla"""
        offset_x, offset_y = self.get_screen_offset()
        return x + offset_x, y + offset_y
    
    def debug_print(self, action, x, y, **kwargs):
        print(f"[DEBUG] {action}: ({x}, {y}) offset=({self.screen_config['screen_offset_x']}, {self.screen_config['screen_offset_y']}) screen={self.screen_config['screen_name']}")

    def click(self, x, y, **kwargs):
        adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
        self.debug_print('click', adjusted_x, adjusted_y)
        return pyautogui.click(adjusted_x, adjusted_y, **kwargs)
    
    def moveTo(self, x, y, **kwargs):
        adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
        self.debug_print('moveTo', adjusted_x, adjusted_y)
        return pyautogui.moveTo(adjusted_x, adjusted_y, **kwargs)
    
    def dragTo(self, x, y, **kwargs):
        adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
        self.debug_print('dragTo', adjusted_x, adjusted_y)
        return pyautogui.dragTo(adjusted_x, adjusted_y, **kwargs)
    
    def screenshot(self, path, region=None, **kwargs):
        with mss.mss() as sct:
            offset_x, offset_y = self.get_screen_offset()
            if region:
                x, y, width, height = region
                monitor = {
                    "left": offset_x + x,
                    "top": offset_y + y,
                    "width": width,
                    "height": height
                }
            else:
                monitor = {
                    "left": offset_x,
                    "top": offset_y,
                    "width": self.screen_config['screen_width'],
                    "height": self.screen_config['screen_height']
                }
            img = sct.grab(monitor)
            mss.tools.to_png(img.rgb, img.size, output=path)
            self.debug_print('screenshot', monitor["left"], monitor["top"])
            return path
    
    def get_current_screen_info(self):
        """Mevcut ekran bilgilerini döndür"""
        return {
            'name': self.screen_config['screen_name'],
            'offset': self.get_screen_offset(),
            'size': self.get_screen_size()
        }
    
    def print_screen_info(self):
        """Ekran bilgilerini yazdır"""
        info = self.get_current_screen_info()
        print(f"📺 Aktif Ekran: {info['name']}")
        print(f"   Offset: {info['offset']}")
        print(f"   Boyut: {info['size']}")

    def get_screen_size_from_config(self):
        return self.screen_config['screen_width'], self.screen_config['screen_height']

# Global screen manager instance
screen_manager = ScreenManager()

# Kolay kullanım için fonksiyonlar
def click(x, y, **kwargs):
    """Ekran offset'i ile tıklama"""
    return screen_manager.click(x, y, **kwargs)

def moveTo(x, y, **kwargs):
    """Ekran offset'i ile fare taşıma"""
    return screen_manager.moveTo(x, y, **kwargs)

def dragTo(x, y, **kwargs):
    """Ekran offset'i ile sürükleme"""
    return screen_manager.dragTo(x, y, **kwargs)

def screenshot(path, region=None, **kwargs):
    """Ekran offset'i ile screenshot"""
    return screen_manager.screenshot(path, region, **kwargs)

def get_screen_info():
    """Ekran bilgilerini döndür"""
    return screen_manager.get_current_screen_info()

def print_screen_info():
    """Ekran bilgilerini yazdır"""
    screen_manager.print_screen_info() 