# Clash of Clans Farming Bot

Bu proje, Clash of Clans oyununda otomatik farming (yağma) yapmak için geliştirilmiş bir Python botudur. Bot, belirli miktarda yağma içeren base'leri bulur ve otomatik olarak saldırır.

## 🚀 Özellikler

- **Otomatik Base Arama**: Belirli yağma miktarlarına göre base arama
- **OCR Teknolojisi**: Ekran görüntüsünden yağma miktarını okuma
- **Çoklu Hesap Desteği**: İki farklı hesap için farklı yağma hedefleri
- **Telegram Kontrol**: Telegram bot üzerinden uzaktan kontrol
- **İstatistik Takibi**: Saldırı sayısı ve zaman bilgileri

## 📋 Gereksinimler

### Sistem Gereksinimleri

- Windows 10/11
- Python 3.8 veya üzeri
- Tesseract-OCR
- Clash of Clans (BlueStacks veya benzeri emülatör)

### Python Kütüphaneleri

```bash
pyautogui>=0.9.54
opencv-python>=4.8.0
Pillow>=10.0.0
pytesseract>=0.3.10
numpy>=1.24.0
python-dotenv>=1.0.0
python-telegram-bot>=20.0
pywin32
mss
```

## 🛠️ Kurulum

### 1. Projeyi İndirin

```bash
git clone <repository-url>
cd coc-farming-bot
```

### 2. Python Kütüphanelerini Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Tesseract-OCR Kurulumu

1. [Tesseract-OCR'ı indirin](https://github.com/UB-Mannheim/tesseract/wiki)
2. `C:\Program Files\Tesseract-OCR\` dizinine kurun
3. Sistem PATH'ine ekleyin

### 4. Çevre Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değerleri düzenleyin:

```env
# Tesseract-OCR dosya yolu
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Ekran görüntüleri için geçici dosya yolu
SCREENSHOT_PATH=temp_screenshot.png

# Telegram Bot Token (BotFather'dan alınacak)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Telegram Bot için izin verilen kullanıcı ID'leri
TELEGRAM_ALLOWED_USERS=123456789,987654321
```

## 🤖 Telegram Bot Kurulumu

### 1. Telegram Bot Oluşturun

1. Telegram'da [@BotFather](https://t.me/botfather) ile konuşun
2. `/newbot` komutunu kullanın
3. Bot adı ve kullanıcı adı belirleyin
4. Size verilen token'ı `.env` dosyasına ekleyin

### 2. Kullanıcı ID'nizi Bulun

1. Telegram'da [@userinfobot](https://t.me/userinfobot) ile konuşun
2. Size verilen ID'yi `.env` dosyasındaki `TELEGRAM_ALLOWED_USERS` kısmına ekleyin

### 3. Botu Başlatın

```bash
python telegram_bot.py
```

veya

```bash
run_telegram_bot.bat
```

## 📱 Telegram Bot Komutları

| Komut | Açıklama |
|-------|----------|
| `/start` | Bot hakkında bilgi ve komut listesi |
| `/help` | Detaylı yardım mesajı |
| `/status` | Bot durumunu gösterir |
| `/start_bot` | Farming botunu başlatır |
| `/stop_bot` | Farming botunu durdurur |
| `/account <1\|2>` | Hesap seçer (1: Ana hesap, 2: İkinci hesap) |
| `/stats` | İstatistikleri gösterir |

## 🎮 Kullanım

### Manuel Kullanım

```bash
python main.py
```

### Telegram ile Kullanım

1. Botu başlatın: `python telegram_bot.py`
2. Telegram'da botunuza mesaj gönderin
3. `/start` komutu ile başlayın
4. `/start_bot` ile farming'i başlatın
5. `/stop_bot` ile farming'i durdurun

## ⚙️ Yapılandırma

### Yağma Hedefleri

- **Hesap 1**: 1.8M+ toplam yağma (Altın + Elixir)
- **Hesap 2**: 1.2M+ toplam yağma (Altın + Elixir)

### Saldırı Stratejileri

- **Hesap 1**: E-Dragon saldırısı
- **Hesap 2**: Dragon saldırısı

## 📊 İstatistikler

Bot aşağıdaki istatistikleri takip eder:

- Toplam saldırı sayısı
- Son saldırı zamanı
- Aktif hesap bilgisi
- Bot çalışma durumu

## ⚠️ Uyarılar

- Bu bot sadece eğitim amaçlıdır
- Gerçek hesaplarda kullanım sorumluluğu size aittir
- Oyun kurallarını ihlal etmemeye dikkat edin
- Düzenli olarak bot durumunu kontrol edin

## 🐛 Sorun Giderme

### Yaygın Sorunlar

#### 1. Tesseract bulunamadı hatası

- Tesseract-OCR'ın doğru kurulduğundan emin olun
- `.env` dosyasındaki `TESSERACT_CMD` yolunu kontrol edin

#### 2. Ekran görüntüsü alınamıyor

- Oyun penceresinin görünür olduğundan emin olun
- Ekran çözünürlüğünü kontrol edin

#### 3. Telegram bot çalışmıyor

- Bot token'ının doğru olduğundan emin olun
- Kullanıcı ID'nizin `TELEGRAM_ALLOWED_USERS` listesinde olduğunu kontrol edin

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için lisans gerekebilir.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📞 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Not**: Bu bot sadece eğitim amaçlıdır. Gerçek hesaplarda kullanım sorumluluğu size aittir.
