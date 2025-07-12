import logging
import os
from typing import Optional, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from dotenv import load_dotenv
import threading
import time
from datetime import datetime

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
            [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
            [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
            [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
            [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
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
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        
        if not update.effective_user or not self.is_authorized(update.effective_user.id):
            await send("❌ Bu botu kullanma yetkiniz yok!")
            return
        
        status_text = f"""
📊 **Bot Durumu**

🔄 **Çalışma Durumu:** {'🟢 Çalışıyor' if self.bot_running else '🔴 Durdu'}
👤 **Aktif Hesap:** {self.current_account}
⚔️ **Toplam Saldırı:** {self.attack_counter}
🕐 **Son Saldırı:** {self.last_attack_time if self.last_attack_time else 'Henüz saldırı yapılmadı'}
        """
        await send(status_text, parse_mode='Markdown', reply_markup=reply_markup)
    
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

    async def startbot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif update.message:
            send = update.message.reply_text
        if not send:
            return
        await send("📱 Clash of Clans başlatılıyor...", parse_mode='Markdown', reply_markup=reply_markup)
        self.launch_clash_of_clans()
        await send("⏳ Oyun yüklenmesi için 30 saniye bekleniyor...", parse_mode='Markdown', reply_markup=reply_markup)
        time.sleep(30)
        self.bot_running = True
        self.bot_thread = threading.Thread(target=self.run_farming_bot)
        self.bot_thread.daemon = True
        self.bot_thread.start()
        await send("🟢 **Bot başlatıldı!** Farming işlemi başladı.", parse_mode='Markdown', reply_markup=reply_markup)

    async def stopbot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
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

    async def account_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False) -> None:
        if not self.is_valid_update(update):
            return
        send = None
        reply_markup = None
        if from_button and update.callback_query:
            send = update.callback_query.edit_message_text
            # Ana menü butonlarını oluştur
            keyboard = [
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
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
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
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
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
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
            await send("🔍 Depo durumu kontrol ediliyor...", parse_mode='Markdown', reply_markup=reply_markup)
            is_full, fullness_percentage = storage_checker.check_storage_fullness()
            if is_full:
                await send(f"⚠️ **Depo Dolu!** ({fullness_percentage:.1f}% dolu) Farming durdurulmalı.", parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await send(f"✅ **Depo Durumu:** {fullness_percentage:.1f}% dolu - Farming devam edebilir.", parse_mode='Markdown', reply_markup=reply_markup)
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
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
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
        elif data == "stats":
            await self.stats_command(update, context, from_button=True)
        elif data == "check_storage":
            await self.check_storage_command(update, context, from_button=True)
        elif data == "storage":
            await self.storage_status_command(update, context, from_button=True)
        elif data == "back_to_main":
            keyboard = [
                [InlineKeyboardButton("🚀 Botu Başlat", callback_data="startbot"), InlineKeyboardButton("⛔ Botu Durdur", callback_data="stopbot")],
                [InlineKeyboardButton("📊 Durum", callback_data="status"), InlineKeyboardButton("👤 Hesap Seç", callback_data="account_menu")],
                [InlineKeyboardButton("📈 İstatistik", callback_data="stats")],
                [InlineKeyboardButton("🏗️ Depo Kontrol", callback_data="check_storage"), InlineKeyboardButton("⚙️ Depo Ayarları", callback_data="storage")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🤖 *Clash of Clans Farming Bot*\n\nKomutları aşağıdaki menüden seçebilirsiniz:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

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