# Clash of Clans Bot – Otomatik Yağma ve Trophy Düşürme 🛡️

## İçindekiler / Table of Contents 

**Türkçe**

* [Giriş](#giriş)
* [Özellikler](#özellikler)
* [Gereksinimler](#gereksinimler)
* [Kurulum](#kurulum)
* [Kullanım](#kullanım)
* [Trophy Düşürücü](#trophy-düşürücü)
* [Saldırı Ordusu Detayları](#saldırı-ordusu-detayları)
* [Gelecek İyileştirmeler](#gelecek-iyileştirmeler)
* [Sorumluluk Reddi](#sorumluluk-reddi)

**English**

* [Introduction](#introduction)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Trophy Deranker](#trophy-deranker-1)
* [Attack Composition Details](#attack-composition-details)
* [Future Improvements](#future-improvements)
* [Disclaimer](#disclaimer)

---

## Türkçe

### Giriş

Clash of Clans için tam otomatik bir yağma botu. Yüksek yağma içeren üsleri OCR teknolojisi ile tespit eder ve otomatik olarak saldırır. Ayrıca trophy düşürmek için ayrı bir araç da dahildir.

Hesap isimleri "MAIN" (1) ve "ALT" (2) **örnek olarak verilmiştir** ve sadece ayırt etmek için kullanılır – kodda istediğiniz gibi değiştirebilirsiniz.

---

### Özellikler

* OCR destekli üs tespiti (Tesseract ile metin tanıma)
* Rastgele pozisyonlarla otomatik saldırılar
* İki hesap modu ile özel yağma eşikleri
* Trophy düşürmek için ayrı araç
* Gerçek zamanlı yağma miktarı analizi
* Akıllı base arama algoritması

---

### Gereksinimler

* **İki monitör önerilir:**
  * Monitör 1: Clash of Clans (Google Play Oyunları Beta üzerinden)
  * Monitör 2: Diğer programları kullanmak için
* **2. Ekran Desteği:** Bot artık 2. ekranda çalışabilir!
* Tek monitör de çalışır – ancak bot yağma sırasında tüm girişleri bloklar
* Windows işletim sistemi
* [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/releases/) kurulu olmalı
* [Google Play Oyunları (Beta)](https://play.google.com/googleplaygames) kurulu olmalı
* Python kütüphaneleri (pip ile kurulum):

```bash
pip install pyautogui opencv-python pytesseract numpy Pillow python-dotenv
```

---

### Kurulum

1. **Tesseract-OCR'ı indirin ve kurun:**
   - [Tesseract-OCR GitHub](https://github.com/tesseract-ocr/tesseract/releases/) adresinden indirin
   - C:\Program Files\Tesseract-OCR\ klasörüne kurun
   - Sistem PATH'ine ekleyin

2. **Çevre değişkenlerini ayarlayın:**
   - `.env` dosyası oluşturun
   - Tesseract yolunu ve screenshot yolunu belirtin

3. **Python kütüphanelerini kurun:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Kullanım

#### **Hızlı Başlangıç:**
1. `run.bat` dosyasını çift tıklayın
2. Giriş olarak `1` (MAIN hesap) veya `2` (ALT hesap) seçin
3. Bot otomatik olarak yeterli yağma içeren üs arayacak
4. İyi bir üs bulunduğunda saldırı otomatik olarak başlayacak

#### **2. Ekran Desteği:**
1. `setup_screen.bat` dosyasını çalıştırın
2. Ekran seçeneklerinden birini seçin:
   - Ana Ekran (varsayılan)
   - İkinci Ekran (1920x1080, 1366x768, 2560x1440, 3840x2160)
   - Manuel ekran seçimi (arayüz ile)
3. `run.bat` ile botu başlatın
4. Bot seçilen ekranda çalışacak

#### **Manuel Çalıştırma:**
```bash
python main.py
```

---

### Trophy Düşürücü

`trophy_deranker.py` scripti **isteğe bağlı ek bir araçtır** ve bilinçli olarak maç kaybederek trophy düşürür.
Düşük trophy bölgelerinde yağma yapmak için idealdir.

---

### Saldırı Ordusu Detayları

#### **MAIN Hesap (Account 1) - E-Dragon Saldırısı**

**Birlikler:**
- **E-Dragonlar:** 10 adet (ana saldırı gücü)
- **Savaş Makinesi:** 1 adet (tank rolü)
- **Kral:** 1 adet (Barbarian King)
- **Kraliçe:** 1 adet (Archer Queen)
- **Muhafız:** 1 adet (Grand Warden)
- **Balonlar:** 2 adet (hava desteği)

**Büyüler:**
- **Rage Büyüsü:** 5 adet (saldırı gücünü artırır)
- **Zap Büyüsü:** 1 adet (savunma yapılarını zayıflatır)

**Saldırı Stratejisi:**
1. Base'in bir köşesinden başlar
2. E-Dragonları o köşe boyunca yerleştirir
3. Kahramanları stratejik noktalara konumlandırır
4. Rage büyülerini saldırı yoluna bırakır
5. Muhafız yeteneğini tetikler
6. Zap büyüsünü base ortasına atar

#### **ALT Hesap (Account 2) - Dragon Saldırısı**

**Birlikler:**
- **Dragonlar:** 10 adet (ana saldırı gücü)
- **Kral:** 1 adet (Barbarian King)

**Büyüler:**
- **Rage Büyüsü:** 3 adet (saldırı gücünü artırır)

**Saldırı Stratejisi:**
1. Base'in bir köşesinden başlar
2. Dragonları o köşe boyunca yerleştirir
3. Kralı stratejik bir noktaya konumlandırır
4. Rage büyülerini saldırı yoluna bırakır
5. Kral yeteneğini tetikler

#### **Saldırı Pozisyonları**
Her saldırı 4 farklı pozisyondan rastgele seçilir:
- **Sağ Üst Köşe**
- **Sol Üst Köşe**
- **Sağ Alt Köşe**
- **Sol Alt Köşe**

#### **Yağma Eşikleri**
- **MAIN Hesap:** Minimum 1.8M toplam yağma (Altın + Elixir)
- **ALT Hesap:** Minimum 1.2M toplam yağma (Altın + Elixir)

#### **Önemli Notlar**
- Bot sadece görsel tıklama yapar, AI kullanmaz
- Karmaşık ordular için kod değişikliği gerekir
- Mükemmel değil ama Netflix izlerken ya da müzik dinlerken rahatlıkla kullanılabilir
- Her saldırıda rastgele gecikmeler eklenir (insan davranışını taklit etmek için)

---

### Gelecek İyileştirmeler

* **AI Entegrasyonu (örn. ChatGPT):**
  * Daha iyi yağma değerlendirmesi
  * Hava savunması ve base yapısı tespiti
  * Daha insansı saldırılar
* Ordular ve yağma eşikleri için daha fazla konfigürasyon seçeneği
* Farklı saldırı stratejileri
* Gerçek zamanlı base analizi

---

### Sorumluluk Reddi

Bu **resmi olmayan bir araçtır** ve **Supercell ile bağlantısı yoktur**.
Kullanım **kendi sorumluluğunuzdadır**. Bot "insansı" davransa da ban riski teorik olarak mümkündür.

---

## English

### Introduction

A fully automated Clash of Clans farming bot that scans loot using OCR and attacks automatically.
A separate tool is included for intentional trophy dropping.

Account names like "MAIN" (1) and "ALT" (2) are **just examples** – feel free to change them in the code.

---

### Features

* OCR-based loot scanning (Tesseract)
* Automated base searching & attacks
* Two account profiles with custom loot requirements
* Optional tool to intentionally lose matches (Trophy Deranker)
* Real-time loot amount analysis
* Smart base searching algorithm

---

### Requirements

* **Dual-monitor setup recommended:**
  * Monitor 1: Clash of Clans running via Google Play Games (Beta)
  * Monitor 2: For multitasking (e.g. browsing, Netflix)
* Single-monitor setup works too, but the bot will block input during farming
* Windows operating system
* Installed [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/releases/) (system path, e.g. C:\Program Files\Tesseract-OCR\tesseract.exe)
* [Google Play Games (Beta)](https://play.google.com/googleplaygames) installed
* Python libraries (install via pip):

```bash
pip install pyautogui opencv-python pytesseract numpy Pillow python-dotenv
```

---

### Installation

1. **Download and install Tesseract-OCR:**
   - Download from [Tesseract-OCR GitHub](https://github.com/tesseract-ocr/tesseract/releases/)
   - Install to C:\Program Files\Tesseract-OCR\
   - Add to system PATH

2. **Set up environment variables:**
   - Create `.env` file
   - Specify Tesseract path and screenshot path

3. **Install Python libraries:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Usage

1. Run `main.py`
2. Select `1` **for MAIN** or `2` **for ALT**
3. The bot will automatically search for a base with sufficient loot
4. Once a good base is found, the attack will start automatically

---

### Trophy Deranker

The **trophy_deranker.py** script is an **optional extra tool** that intentionally loses matches to drop trophies.
It is ideal for farming in low trophy ranges.

---

### Attack Composition Details

#### **MAIN Account (Account 1) - E-Dragon Attack**

**Troops:**
- **E-Dragons:** 10 units (main attack force)
- **War Machine:** 1 unit (tank role)
- **King:** 1 unit (Barbarian King)
- **Queen:** 1 unit (Archer Queen)
- **Warden:** 1 unit (Grand Warden)
- **Balloons:** 2 units (air support)

**Spells:**
- **Rage Spell:** 5 units (increases attack power)
- **Zap Spell:** 1 unit (weakens defense structures)

**Attack Strategy:**
1. Starts from one corner of the base
2. Places E-Dragons along that corner
3. Positions heroes at strategic points
4. Drops Rage spells along the attack path
5. Activates Warden ability
6. Casts Zap spell in the center of the base

#### **ALT Account (Account 2) - Dragon Attack**

**Troops:**
- **Dragons:** 10 units (main attack force)
- **King:** 1 unit (Barbarian King)

**Spells:**
- **Rage Spell:** 3 units (increases attack power)

**Attack Strategy:**
1. Starts from one corner of the base
2. Places Dragons along that corner
3. Positions King at a strategic point
4. Drops Rage spells along the attack path
5. Activates King ability

#### **Attack Positions**
Each attack randomly selects from 4 different positions:
- **Top Right Corner**
- **Top Left Corner**
- **Bottom Right Corner**
- **Bottom Left Corner**

#### **Loot Thresholds**
- **MAIN Account:** Minimum 1.8M total loot (Gold + Elixir)
- **ALT Account:** Minimum 1.2M total loot (Gold + Elixir)

#### **Important Notes**
- Bot only performs visual clicking, no AI used
- Code modification required for complex armies
- Not perfect but good enough for casual Netflix watching or music listening
- Random delays added to each attack (to mimic human behavior)

---

### Future Improvements

* **AI integration (e.g. ChatGPT) to:**
  * **Better loot evaluation**
  * **Air defense & base structure detection**
  * **More human-like attacks**
* More configuration options for troops and loot thresholds
* Different attack strategies
* Real-time base analysis

---

### Disclaimer

This is an **unofficial tool** and is **not affiliated with Supercell**.
Use at your own risk. A ban is possible, even though the bot acts "human-like".

