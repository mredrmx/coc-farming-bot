# 🤖 Telegram Bot Kurulum Rehberi

Bu rehber, Clash of Clans Farming Bot'unu Telegram üzerinden kontrol etmek için gerekli adımları açıklar.

## 📋 Gereksinimler

- Telegram hesabı
- Python 3.8 veya üzeri
- `python-telegram-bot` kütüphanesi

## 🚀 Adım Adım Kurulum

### 1. Telegram Bot Oluşturma

1. **BotFather'a Gidin**

   - Telegram'da [@BotFather](https://t.me/botfather) ile konuşun
   - `/start` komutunu gönderin

2. **Yeni Bot Oluşturun**

   - `/newbot` komutunu gönderin
   - Bot için bir isim girin (örn: "CoC Farming Bot")
   - Bot için bir kullanıcı adı girin (örn: "coc_farming_bot")
   - Kullanıcı adı `_bot` ile bitmelidir

3. **Bot Token'ını Kaydedin**

   - BotFather size bir token verecek
   - Bu token'ı güvenli bir yere kaydedin
   - Örnek: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Kullanıcı ID'nizi Bulma

1. **UserInfoBot'a Gidin**

   - Telegram'da [@userinfobot](https://t.me/userinfobot) ile konuşun
   - `/start` komutunu gönderin
   - Size verilen ID'yi kaydedin (örn: `123456789`)

### 3. Çevre Değişkenlerini Ayarlama

1. **`.env` Dosyasını Düzenleyin**

   ```env
   # Mevcut ayarlar
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   SCREENSHOT_PATH=temp_screenshot.png

   # Telegram Bot Ayarları
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_ALLOWED_USERS=123456789
   ```

2. **Birden Fazla Kullanıcı Ekleme**

   - Virgülle ayırarak birden fazla kullanıcı ID'si ekleyebilirsiniz
   - Örnek: `TELEGRAM_ALLOWED_USERS=123456789,987654321,555666777`

### 4. Botu Test Etme

1. **Botu Başlatın**

   ```bash
   python telegram_bot.py
   ```

2. **Telegram'da Test Edin**

   - Botunuza mesaj gönderin
   - `/start` komutunu gönderin
   - Bot size hoş geldin mesajı göndermelidir

## 📱 Bot Komutları

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `/start` | Bot hakkında bilgi | `/start` |
| `/help` | Yardım mesajı | `/help` |
| `/status` | Bot durumu | `/status` |
| `/start_bot` | Farming'i başlat | `/start_bot` |
| `/stop_bot` | Farming'i durdur | `/stop_bot` |
| `/account` | Hesap seç | `/account 1` |
| `/stats` | İstatistikler | `/stats` |

## 🔧 Sorun Giderme

### Bot Yanıt Vermiyor

1. Bot token'ının doğru olduğundan emin olun
2. Bot'un çalıştığından emin olun
3. Kullanıcı ID'nizin `TELEGRAM_ALLOWED_USERS` listesinde olduğunu kontrol edin

### "Bu botu kullanma yetkiniz yok!" Hatası

1. Kullanıcı ID'nizi doğru aldığınızdan emin olun
2. `.env` dosyasındaki `TELEGRAM_ALLOWED_USERS` listesini kontrol edin
3. ID'lerin virgülle ayrıldığından emin olun

### Bot Başlatılamıyor

1. Python kütüphanelerinin kurulu olduğundan emin olun
2. `.env` dosyasının doğru konumda olduğunu kontrol edin
3. Hata mesajlarını kontrol edin

## 🔒 Güvenlik

- Bot token'ınızı kimseyle paylaşmayın
- Sadece güvendiğiniz kullanıcıları `TELEGRAM_ALLOWED_USERS` listesine ekleyin
- Bot'u güvenli bir ortamda çalıştırın

## 📞 Destek

Sorun yaşarsanız:

1. Hata mesajlarını kontrol edin
2. Bot loglarını inceleyin
3. GitHub Issues'da sorun bildirin

---

**Not**: Bu bot sadece eğitim amaçlıdır. Gerçek hesaplarda kullanım sorumluluğu size aittir.
