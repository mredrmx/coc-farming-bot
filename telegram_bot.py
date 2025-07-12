import logging
import os
import asyncio
from typing import Optional, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from dotenv import load_dotenv
import threading
import time
from datetime import datetime
import psutil

# Çevre değişkenlerini yükle
load_dotenv()

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBotController:
    def __init__(self) -> None:
        self.bot_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
        allowed_users_str: str = os.getenv("TELEGRAM_ALLOWED_USERS", "")
        self.allowed_users: List[int] = [
            int(user_id.strip()) for user_id in allowed_users_str.split(",") 
            if user_id.strip()
        ]
        
        # Bot durumu değişkenleri
        self.bot_running: bool = False
        self.bot_thread: Optional[threading.Thread] = None
        self.current_account: str = "1"
        self.attack_counter: int = 0
        self.last_attack_time: Optional[str] = None
        
        # Screenshot mesaj takibi için sözlük
        self.screenshot_messages: dict = {}  # {chat_id: message_id}
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN çevre değişkeni bulunamadı!")
        
        if not self.allowed_users:
            raise ValueError("TELEGRAM_ALLOWED_USERS çevre değişkeni bulunamadı!")
    
    def is_authorized(self, user_id: int) -> bool:
        """Kullanıcının yetkili olup olmadığını kontrol eder"""
        return user_id in self.allowed_users
    
    def is_valid_update(self, update: Update) -> bool:
        """Update'in geçerli olup olmadığını kontrol eder"""
        return (update.message is not None or update.callback_query is not None) and update.effective_user is not None
    
    def get_coc_button_text(self) -> str:
        """COC durumuna göre buton metnini döndür"""
        return "🎮 CoC Başlat" if not self.is_coc_running() else "🔄 CoC Kapat"
    
    def get_coc_button_callback(self) -> str:
        """COC durumuna göre callback data döndür"""
        return "launch_coc" if not self.is_coc_running() else "close_coc"
    
    def get_bot_button_text(self) -> str:
        """Bot durumuna göre buton metnini döndür"""
        return "🚀 Botu Başlat" if not self.bot_running else "⛔ Botu Durdur"
    
    def get_bot_button_callback(self) -> str:
        """Bot durumuna göre callback data döndür"""
        return "startbot" if not self.bot_running else "stopbot"
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Bot başlatma komutu - Ana menü (inline keyboard ile)"""
        if not self.is_valid_update(update):
            return
        assert update.message is not None
        assert update.effective_user is not None
        
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Bu botu kullanma yetkiniz yok!")
            return
        
        keyboard = [
            [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
            [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
            [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
            [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🤖 *Clash of Clans Farming Bot*\n\nKomutları aşağıdaki menüden seçebilirsiniz:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        """Bot durumu komutu"""
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        if not update.effective_user or not self.is_authorized(update.effective_user.id):
            await send("❌ Bu botu kullanma yetkiniz yok!")
            return
        
        coc_status = '🟢 Açık' if self.is_coc_running() else '🔴 Kapalı'
        status_text = f"""
📊 **Bot Durumu**

🔄 **Çalışma Durumu:** {'🟢 Çalışıyor' if self.bot_running else '🔴 Durdu'}
🎮 **Clash of Clans:** {coc_status}
👤 **Aktif Hesap:** {self.current_account}
⚔️ **Toplam Saldırı:** {self.attack_counter}
🕐 **Son Saldırı:** {self.last_attack_time if self.last_attack_time else 'Henüz saldırı yapılmadı'}
🕐 **Son Güncelleme:** {datetime.now().strftime('%H:%M:%S')}
        """
        await send(status_text, parse_mode='Markdown', reply_markup=reply_markup)
        
        # Durum sayfasında otomatik yenileme için task başlat
        if from_button and update.callback_query:
            asyncio.create_task(self.auto_refresh_status(update, context))
    
    def launch_clash_of_clans(self):
        """Clash of Clans'ı masaüstü kısayolundan başlat"""
        import subprocess
        # Clash of Clans kısayolunun tam yolu
        coc_shortcut = r"C:\Users\Emre\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Google Play Games\Clash of Clans.lnk"
        try:
            # Kısayol ile CoC başlat (shell=True ile .lnk dosyaları çalıştırılabilir)
            subprocess.Popen(coc_shortcut, shell=True)
            logger.info("Clash of Clans masaüstü kısayolundan başlatıldı.")
        except Exception as e:
            logger.error(f"Clash of Clans başlatılamadı: {e}")

    async def launch_coc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        """Clash of Clans'ı başlatma komutu"""
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        await send("🎮 Clash of Clans başlatılıyor...", parse_mode='Markdown', reply_markup=reply_markup)
        try:
            self.launch_clash_of_clans()
            await send("✅ **Clash of Clans başlatıldı!** Oyun yüklenmesi için bekleyin.", parse_mode='Markdown', reply_markup=reply_markup)
            
            # 3 saniye sonra durum sayfasına geç
            if from_button and update.callback_query:
                await asyncio.sleep(3)
                await self.status_command(update, context, from_button=True)
        except Exception as e:
            await send(f"❌ **Hata:** Clash of Clans başlatılamadı: {e}", parse_mode='Markdown', reply_markup=reply_markup)

    async def close_coc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        """Clash of Clans'ı kapatma komutu"""
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        if not self.is_coc_running():
            await send("⚠️ Clash of Clans zaten kapalı!", parse_mode='Markdown', reply_markup=reply_markup)
            return
        
        await send("🔄 Clash of Clans kapatılıyor...", parse_mode='Markdown', reply_markup=reply_markup)
        try:
            if self.close_clash_of_clans():
                await send("✅ **Clash of Clans kapatıldı!**", parse_mode='Markdown', reply_markup=reply_markup)
                
                # 3 saniye sonra durum sayfasına geç
                if from_button and update.callback_query:
                    await asyncio.sleep(3)
                    await self.status_command(update, context, from_button=True)
            else:
                await send("❌ **Hata:** Clash of Clans kapatılamadı!", parse_mode='Markdown', reply_markup=reply_markup)
        except Exception as e:
            await send(f"❌ **Hata:** Clash of Clans kapatılırken hata oluştu: {e}", parse_mode='Markdown', reply_markup=reply_markup)

    async def screenshot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        """Anlık ekran görüntüsü alma komutu"""
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        await send("📸 Ekran görüntüsü alınıyor...", parse_mode='Markdown', reply_markup=reply_markup)
        try:
            from screen_utils import screenshot
            import os
            import glob
            from PIL import Image
            
            # Önceki telegram screenshot dosyalarını temizle
            try:
                old_screenshots_png = glob.glob("telegram_screenshot_*.png")
                old_screenshots_jpg = glob.glob("telegram_screenshot_*.jpg")
                old_temp_files = glob.glob("temp_screenshot_*.png")
                
                all_old_files = old_screenshots_png + old_screenshots_jpg + old_temp_files
                
                for old_file in all_old_files:
                    try:
                        os.remove(old_file)
                        logger.info(f"Eski screenshot dosyası silindi: {old_file}")
                    except Exception as cleanup_error:
                        logger.warning(f"Eski screenshot dosyası silinemedi: {old_file} - {cleanup_error}")
            except Exception as cleanup_error:
                logger.warning(f"Screenshot temizleme hatası: {cleanup_error}")
            
            # Screenshot dosya adını oluştur (JPEG formatı için)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"telegram_screenshot_{timestamp}.jpg"
            
            # Ekran görüntüsü al (önce PNG olarak)
            temp_png_path = f"temp_screenshot_{timestamp}.png"
            screenshot(temp_png_path)
            
            # Görüntü kalitesini 480p'ye düşür ve JPEG'e çevir
            try:
                with Image.open(temp_png_path) as img:
                    # Orijinal boyutları al
                    original_width, original_height = img.size
                    
                    # 360p için yeni boyutları hesapla (aspect ratio korunarak)
                    target_height = 360
                    target_width = int((original_width / original_height) * target_height)
                    
                    # Görüntüyü yeniden boyutlandır
                    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Optimize edilmiş JPEG olarak kaydet (daha küçük dosya boyutu)
                    resized_img.save(screenshot_path, 'JPEG', quality=85, optimize=True)
                    
                    logger.info(f"Screenshot boyutlandırıldı: {original_width}x{original_height} -> {target_width}x{target_height} (JPEG)")
                    
                    # Geçici PNG dosyasını sil
                    try:
                        os.remove(temp_png_path)
                    except:
                        pass
                        
            except Exception as resize_error:
                logger.warning(f"Screenshot boyutlandırma hatası: {resize_error}")
                # Boyutlandırma başarısız olursa orijinal PNG dosyasını kullan
                screenshot_path = temp_png_path
            
            # Dosyanın var olduğunu kontrol et
            if os.path.exists(screenshot_path):
                # Dosyayı Telegram'a gönder
                try:
                    with open(screenshot_path, 'rb') as photo_file:
                        if from_button and update.callback_query and update.callback_query.message:
                            chat_id = update.callback_query.message.chat.id
                            # Önceki screenshot mesajını sil
                            await self.delete_previous_screenshot(chat_id, context)
                            
                            # Yeni screenshot gönder
                            sent_message = await context.bot.send_photo(
                                chat_id=chat_id,
                                photo=photo_file,
                                caption=f"📸 **Anlık Ekran Görüntüsü**\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                                parse_mode='Markdown'
                            )
                            # Yeni mesaj ID'sini kaydet
                            self.screenshot_messages[chat_id] = sent_message.message_id
                            await send("✅ **Ekran görüntüsü gönderildi!**", parse_mode='Markdown', reply_markup=reply_markup)
                            
                            # 3 saniye sonra durum sayfasına geç
                            await asyncio.sleep(3)
                            await self.status_command(update, context, from_button=True)
                        elif update.message:
                            chat_id = update.message.chat.id
                            # Önceki screenshot mesajını sil
                            await self.delete_previous_screenshot(chat_id, context)
                            
                            # Yeni screenshot gönder
                            sent_message = await context.bot.send_photo(
                                chat_id=chat_id,
                                photo=photo_file,
                                caption=f"📸 **Anlık Ekran Görüntüsü**\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                                parse_mode='Markdown'
                            )
                            # Yeni mesaj ID'sini kaydet
                            self.screenshot_messages[chat_id] = sent_message.message_id
                except Exception as photo_error:
                    await send(f"❌ **Hata:** Fotoğraf gönderilrken hata: {photo_error}", parse_mode='Markdown', reply_markup=reply_markup)
                
                # Geçici dosyayı sil
                try:
                    os.remove(screenshot_path)
                    logger.info(f"Yeni screenshot dosyası silindi: {screenshot_path}")
                except Exception as delete_error:
                    logger.warning(f"Yeni screenshot dosyası silinemedi: {screenshot_path} - {delete_error}")
            else:
                await send("❌ **Hata:** Ekran görüntüsü alınamadı!", parse_mode='Markdown', reply_markup=reply_markup)
                
        except Exception as e:
            await send(f"❌ **Hata:** Ekran görüntüsü alınırken hata oluştu: {e}", parse_mode='Markdown', reply_markup=reply_markup)

    async def startbot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        #Botu başlat
        self.bot_running = True
        self.bot_thread = threading.Thread(target=self.run_farming_bot)
        self.bot_thread.daemon = True
        self.bot_thread.start()
        await send("🟢 **Bot başlatıldı!** Farming işlemi başladı.", parse_mode='Markdown', reply_markup=reply_markup)
        
        # 3 saniye sonra durum sayfasına geç
        if from_button and update.callback_query:
            await asyncio.sleep(3)
            await self.status_command(update, context, from_button=True)

    async def stopbot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        if not self.bot_running:
            await send("⚠️ Bot zaten durmuş!", parse_mode='Markdown', reply_markup=reply_markup)
            return
        self.bot_running = False
        await send("🔴 **Bot durduruldu!** Farming işlemi sonlandırıldı.", parse_mode='Markdown', reply_markup=reply_markup)
        
        # 3 saniye sonra durum sayfasına geç
        if from_button and update.callback_query:
            await asyncio.sleep(3)
            await self.status_command(update, context, from_button=True)

    async def account_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        if not context.args:
            await send("❌ Lütfen hesap numarasını belirtin! (1 veya 2)", parse_mode='Markdown', reply_markup=reply_markup)
            return
        account = context.args[0]
        if account not in ["1", "2"]:
            await send("❌ Geçersiz hesap numarası! 1 veya 2 kullanın.", parse_mode='Markdown', reply_markup=reply_markup)
            return
        self.current_account = account
        account_name = "Ana Hesap" if account == "1" else "İkinci Hesap"
        await send(f"✅ **Hesap değiştirildi:** {account_name} (Hesap {account})", parse_mode='Markdown', reply_markup=reply_markup)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback())],
                [InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback()), InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        stats_text = f"""
📈 **Farming İstatistikleri**

⚔️ **Toplam Saldırı:** {self.attack_counter}
🕐 **Son Saldırı:** {self.last_attack_time if self.last_attack_time else 'Henüz saldırı yapılmadı'}
📅 **Bot Başlangıcı:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        """
        await send(stats_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def check_storage_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        try:
            from storage_checker import storage_checker
            await send("🔍 Depo durumu kontrol ediliyor...", parse_mode='Markdown', reply_markup=reply_markup)
            
            # Detaylı depo bilgilerini al
            is_full, fullness_percentage = storage_checker.check_storage_fullness()
            
            # Altın ve Elixir değerlerini al (storage_checker'dan)
            try:
                # Depo kontrolü yaparak değerleri al
                from screen_utils import screenshot
                storage_path = "storage_screenshot.png"
                screenshot(storage_path, region=(1660, 20, 260, 180))
                
                # OCR ile değerleri oku
                import cv2
                import numpy as np
                import pytesseract
                from PIL import Image
                
                cv2_image = cv2.imread(storage_path)
                if cv2_image is not None:
                    hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
                    lower_white = np.array([0, 0, 200])
                    upper_white = np.array([180, 60, 255])
                    mask = cv2.inRange(hsv, lower_white, upper_white)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                    mask_pil = Image.fromarray(mask)
                    
                    result = pytesseract.image_to_string(
                        mask_pil, 
                        timeout=2, 
                        lang='eng',
                        config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789'
                    )
                    
                    lines = [line.strip() for line in result.split('\n') if line.strip()]
                    if len(lines) >= 2:
                        gold_amount = int(lines[0]) if lines[0].isdigit() else 0
                        elixir_amount = int(lines[1]) if lines[1].isdigit() else 0
                        gold_text = f"{gold_amount:,}"
                        elixir_text = f"{elixir_amount:,}"
                    else:
                        gold_text = "Bilinmiyor"
                        elixir_text = "Bilinmiyor"
                else:
                    gold_text = "Bilinmiyor"
                    elixir_text = "Bilinmiyor"
                
                # Geçici dosyayı temizle
                try:
                    os.remove(storage_path)
                except:
                    pass
                    
            except Exception as e:
                logger.warning(f"Altın/Elixir değerleri alınamadı: {e}")
                gold_text = "Bilinmiyor"
                elixir_text = "Bilinmiyor"
            
            if is_full:
                storage_text = f"""
⚠️ **Depo Dolu!** ({fullness_percentage:.1f}% dolu)

💰 **Altın:** {gold_text}
🧪 **Elixir:** {elixir_text}
📊 **Doluluk:** {fullness_percentage:.1f}%

🛑 **Farming durdurulmalı!**
                """
            else:
                storage_text = f"""
✅ **Depo Durumu:** {fullness_percentage:.1f}% dolu

💰 **Altın:** {gold_text}
🧪 **Elixir:** {elixir_text}
📊 **Doluluk:** {fullness_percentage:.1f}%

✅ **Farming devam edebilir.**
                """
            
            await send(storage_text, parse_mode='Markdown', reply_markup=reply_markup)
        except Exception as e:
            await send(f"❌ Depo kontrolü sırasında hata: {e}", parse_mode='Markdown', reply_markup=reply_markup)

    async def storage_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback())],
                [InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback()), InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        try:
            from storage_checker import storage_checker
            status_text = f"""
🏗️ **Depo Durumu**

📊 **Kontrol Sıklığı:** Her {storage_checker.check_interval} saldırıda bir
🔢 **Mevcut Saldırı Sayısı:** {storage_checker.get_current_count()}
📦 **Depo Kapasitesi:** {storage_checker.storage_capacity:,}
⚠️ **Durma Eşiği:** %90 doluluk
            """
            await send(status_text, parse_mode='Markdown', reply_markup=reply_markup)
        except Exception as e:
            await send(f"❌ Depo durumu alınırken hata: {e}", parse_mode='Markdown', reply_markup=reply_markup)
    
    def run_farming_bot(self) -> None:
        """Farming bot ana döngüsü"""
        try:
            from base_search import searchforbase
            from screen_utils import print_screen_info
            from storage_checker import storage_checker
            
            print_screen_info()
            logger.info("🏗️ Depo kontrol sistemi aktif - Her 10 saldırıda bir kontrol")
            
            while self.bot_running:
                try:
                    searchforbase(self.current_account)
                    self.attack_counter += 1
                    self.last_attack_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                    
                    # Her 10 saldırıda bir depo kontrolü
                    if storage_checker.should_check_storage():
                        logger.info(f"🔍 {self.attack_counter}. saldırı sonrası depo kontrolü yapılıyor...")
                        
                        is_full, fullness_percentage = storage_checker.check_storage_fullness()
                        if is_full:
                            logger.warning(f"⚠️ Depo dolu! ({fullness_percentage:.1f}% doluluk) Farming durduruluyor...")
                            self.bot_running = False
                            break
                        else:
                            logger.info(f"✅ Depo kontrolü başarılı ({fullness_percentage:.1f}% dolu) - Farming devam ediyor")
                    
                    time.sleep(5)  # 5 saniye bekle
                except Exception as e:
                    logger.error(f"Farming bot hatası: {e}")
                    time.sleep(10)
                    
        except Exception as e:
            logger.error(f"Farming bot başlatma hatası: {e}")
            self.bot_running = False
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Bilinmeyen mesajları işle"""
        if not self.is_valid_update(update):
            return
        assert update.message is not None
        assert update.effective_user is not None
        
        if not self.is_authorized(update.effective_user.id):
            return
        
        await update.message.reply_text("❓ Bilinmeyen komut. /start yazarak mevcut komutları görebilirsiniz.")
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Inline keyboard buton handler"""
        query = getattr(update, 'callback_query', None)
        if query is None:
            return
        
        # Yetki kontrolü
        if not update.effective_user or not self.is_authorized(update.effective_user.id):
            await query.answer("❌ Bu botu kullanma yetkiniz yok!")
            return
        
        await query.answer()
        data = query.data
        if data == "startbot":
            await self.startbot_command(update, context, from_button=True)
        elif data == "stopbot":
            await self.stopbot_command(update, context, from_button=True)
        elif data == "launch_coc":
            await self.launch_coc_command(update, context, from_button=True)
        elif data == "close_coc":
            await self.close_coc_command(update, context, from_button=True)
        elif data == "screenshot":
            await self.screenshot_command(update, context, from_button=True)
        elif data == "status":
            await self.status_command(update, context, from_button=True)
        elif data == "account_menu":
            keyboard = [
                [InlineKeyboardButton("1 - Ana Hesap", callback_data="account_1"), InlineKeyboardButton("2 - İkinci Hesap", callback_data="account_2")],
                [InlineKeyboardButton("🔙 Ana Menüye Dön", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("👤 Hesap seçimi:", reply_markup=reply_markup)
        elif data == "account_1":
            context.args = ["1"]
            await self.account_command(update, context, from_button=True)
        elif data == "account_2":
            context.args = ["2"]
            await self.account_command(update, context, from_button=True)
        elif data == "check_storage":
            await self.check_storage_command(update, context, from_button=True)
        elif data == "back_to_main":
            keyboard = [
                [InlineKeyboardButton(self.get_bot_button_text(), callback_data=self.get_bot_button_callback()), InlineKeyboardButton(self.get_coc_button_text(), callback_data=self.get_coc_button_callback())],
                [InlineKeyboardButton("📸 Anlık Görüntü", callback_data="screenshot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🤖 *Clash of Clans Farming Bot*\n\nKomutları aşağıdaki menüden seçebilirsiniz:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

    def is_coc_running(self) -> bool:
        """Clash of Clans uygulaması çalışıyor mu kontrol et"""
        for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
            try:
                pname = proc.info['name'] or ''
                pexe = proc.info['exe'] or ''
                pcmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # Google Play Games üzerinden çalışan Clash of Clans'ı kontrol et
                if (
                    'clashofclans' in pcmd.lower()
                    or 'clashofclans' in pexe.lower()
                    or ('Service.exe' in pname and 'googleplaygames' in pcmd.lower())
                ):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    async def auto_refresh_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Durum sayfasını otomatik olarak yeniler"""
        try:
            while True:
                # 10 saniye bekle
                await asyncio.sleep(10)
                
                # Durum sayfasını yenile
                await self.status_command(update, context, from_button=True)
        except Exception as e:
            logger.warning(f"Otomatik durum yenileme hatası: {e}")

    async def delete_previous_screenshot(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Önceki screenshot mesajını sil"""
        try:
            if chat_id in self.screenshot_messages:
                old_message_id = self.screenshot_messages[chat_id]
                await context.bot.delete_message(chat_id=chat_id, message_id=old_message_id)
                logger.info(f"Önceki screenshot mesajı silindi: Chat {chat_id}, Message {old_message_id}")
                # Silinen mesaj ID'sini sözlükten kaldır
                del self.screenshot_messages[chat_id]
        except Exception as e:
            logger.warning(f"Önceki screenshot mesajı silinemedi: Chat {chat_id} - {e}")

    def close_clash_of_clans(self) -> bool:
        """Clash of Clans uygulamasını kapat"""
        closed_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                pname = proc.info['name'] or ''
                pexe = proc.info['exe'] or ''
                pcmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # Google Play Games üzerinden çalışan Clash of Clans'ı bul ve kapat
                if (
                    'clashofclans' in pcmd.lower()
                    or 'clashofclans' in pexe.lower()
                    or ('Service.exe' in pname and 'googleplaygames' in pcmd.lower())
                ):
                    proc.terminate()
                    closed_count += 1
                    logger.info(f"Clash of Clans process'i kapatıldı: PID {proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return closed_count > 0

    def run(self) -> None:
        """Botu çalıştır"""
        if not self.bot_token:
            logger.error("Bot token bulunamadı!")
            return
            
        # Bot uygulamasını oluştur
        application = Application.builder().token(self.bot_token).build()
        
        # Komut işleyicilerini ekle
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("startbot", self.startbot_command))
        application.add_handler(CommandHandler("stopbot", self.stopbot_command))
        application.add_handler(CommandHandler("account", self.account_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("check_storage", self.check_storage_command))
        application.add_handler(CommandHandler("storage", self.storage_status_command))
        application.add_handler(CommandHandler("screenshot", self.screenshot_command))
        
        # Bilinmeyen mesajları işle
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Botu başlat
        logger.info("🤖 Telegram bot başlatılıyor...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main() -> None:
    """Ana fonksiyon"""
    try:
        bot_controller = TelegramBotController()
        bot_controller.run()
    except Exception as e:
        logger.error(f"Telegram bot hatası: {e}")

if __name__ == "__main__":
    main() 