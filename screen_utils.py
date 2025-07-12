#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash of Clans Bot - Ekran Yardımcı Modülü
Clash of Clans Bot - Screen Utilities
"""

import json
import os
import time
import threading
import psutil
import pyautogui
import mss
import mss.tools

class ScreenManager:
    def __init__(self):
        self.config_file = 'screen_config.json'
        self.screen_config = self.load_config()
        
        # Process kontrolü cache'i
        self._coc_process_cache = None
        self._cache_timestamp = 0
        self._cache_duration = 30  # 30 saniye cache süresi
        
        # Thread güvenliği
        self._lock = threading.Lock()
        
        # Performans iyileştirmeleri
        self._last_screenshot_time = 0
        self._screenshot_cooldown = 0.1  # 100ms screenshot arası bekleme
        
        # PyAutoGUI güvenlik ayarları
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1  # Tıklama arası minimum bekleme
    
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
        """Thread-safe tıklama işlemi"""
        with self._lock:
            adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
            self.debug_print('click', adjusted_x, adjusted_y)
            return pyautogui.click(adjusted_x, adjusted_y, **kwargs)
    
    def moveTo(self, x, y, **kwargs):
        """Thread-safe fare taşıma işlemi"""
        with self._lock:
            adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
            self.debug_print('moveTo', adjusted_x, adjusted_y)
            return pyautogui.moveTo(adjusted_x, adjusted_y, **kwargs)
    
    def dragTo(self, x, y, **kwargs):
        """Thread-safe sürükleme işlemi"""
        with self._lock:
            adjusted_x, adjusted_y = self.adjust_coordinates(x, y)
            self.debug_print('dragTo', adjusted_x, adjusted_y)
            return pyautogui.dragTo(adjusted_x, adjusted_y, **kwargs)
    
    def screenshot(self, path, region=None, **kwargs):
        """Thread-safe screenshot işlemi"""
        with self._lock:
            # Screenshot cooldown kontrolü
            current_time = time.time()
            if current_time - self._last_screenshot_time < self._screenshot_cooldown:
                time.sleep(self._screenshot_cooldown - (current_time - self._last_screenshot_time))
            
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
                self._last_screenshot_time = time.time()
                return path
    
    def is_coc_running(self):
        """Clash of Clans'ın çalışıp çalışmadığını kontrol eder (cache'li)"""
        current_time = time.time()
        
        # Cache kontrolü
        if (self._coc_process_cache is not None and 
            current_time - self._cache_timestamp < self._cache_duration):
            return self._coc_process_cache
        
        # Process kontrolü
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'clash' in proc.info['name'].lower():
                    self._coc_process_cache = True
                    self._cache_timestamp = current_time
                    return True
            self._coc_process_cache = False
            self._cache_timestamp = current_time
            return False
        except Exception as e:
            print(f"Process kontrolü hatası: {e}")
            return False
    
    def clear_process_cache(self):
        """Process cache'ini temizler"""
        with self._lock:
            self._coc_process_cache = None
            self._cache_timestamp = 0
    
    def set_cache_duration(self, duration):
        """Cache süresini ayarlar"""
        with self._lock:
            self._cache_duration = max(1, duration)
    
    def set_screenshot_cooldown(self, cooldown):
        """Screenshot arası bekleme süresini ayarlar"""
        with self._lock:
            self._screenshot_cooldown = max(0.01, cooldown)
    
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

def is_coc_running():
    """Clash of Clans'ın çalışıp çalışmadığını kontrol eder"""
    return screen_manager.is_coc_running()

def get_screen_info():
    """Ekran bilgilerini döndür"""
    return screen_manager.get_current_screen_info()

def print_screen_info():
    """Ekran bilgilerini yazdır"""
    screen_manager.print_screen_info() 