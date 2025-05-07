# Clash of Clans Bot – Automatisiertes Farming & Trophy-Deranking 🛡️

# Clash of Clans Bot – Automated Farming & Trophy Deranking 🛡️

---

## Inhaltsverzeichnis / Table of Contents 

**Deutsch**

* [Einleitung](#einleitung)
* [Funktionen](#funktionen)
* [Systemvoraussetzungen](#systemvoraussetzungen)
* [Verwendung](#verwendung)
* [Trophy Deranker](#trophy-deranker)
* [Hinweise zur Angriffskomposition](#hinweise-zur-angriffskomposition)
* [Zukünftige Verbesserungen](#zukünftige-verbesserungen)
* [Haftungsausschluss](#haftungsausschluss)



**English**

* [Introduction](#introduction)
* [Features](#features)
* [System Requirements](#system-requirements)
* [Usage](#usage)
* [Trophy Deranker](#trophy-deranker-1)
* [Attack Composition Notes](#attack-composition-notes)
* [Future Improvements](#future-improvements)
* [Disclaimer](#disclaimer)

---

## Deutsch

### Einleitung

Ein vollautomatisierter Bot für Clash of Clans, der Basen mit hohem Loot erkennt und automatisch angreift. Zusätzlich ist ein separates Tool enthalten, das gezielt Trophäen reduziert.

Die Accountnamen „MAIN“ bzw. "1" und „ALT“ bzw. "2" sind **frei gewählt** und dienen nur der Unterscheidung – sie können im Code beliebig angepasst werden.

---

### Funktionen

* OCR-gestützte Basenerkennung (Texterkennung via Tesseract)
* Automatisierte Angriffe mit zufälliger Position
* Zwei Account-Modi mit individuellen Loot-Schwellen (nicht verpflichtend)
* Separater Trophy-Deranker für gezielten Pokalverlust

---

### Systemvoraussetzungen

* Zwei Monitore empfohlen:

  * Monitor 1: Clash of Clans läuft über Google Play Spiele (Beta)
  * Monitor 2: Für gleichzeitige Nutzung anderer Programme
* Ein Monitor funktioniert ebenfalls – allerdings blockiert der Bot alle Eingaben während des Farmens
* Windows-Betriebssystem
* Installiertes [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/releases/ "Tesseract-OCR GitHub Downloads")
 (Systempfad, z.B. C:\Program Files\Tesseract-OCR\tesseract.exe)
* Python-Bibliotheken (per pip install):

```bash
pyautogui cv2 pytesseract numpy Pillow
```

---

### Verwendung

1. Starte `main.py`
2. Wähle per Eingabe `1` **für MAIN** oder `2` **für ALT**
3. Der Bot sucht automatisch nach einer Base mit ausreichendem Loot
4. Wird eine gute Base gefunden, startet der Angriff – vollautomatisch

---

### Trophy Deranker

Das Skript **trophy\_deranker.py** ist ein **optionales Extra-Tool**, das bewusst Matches verliert, um Trophäen zu reduzieren.
Es ist ideal, um gezielt in niedrigen Pokalregionen zu farmen.

---

### Hinweise zur Angriffskomposition

* **Account „MAIN“**:

  * Truppen: E-Dragons, Ballons, Warden, Queen & King
  * Zauber: Rage, Zap

* **Account „ALT“**:

  * Truppen: Dragons, King
  * Zauber: Rage, Zap
  * (minimalistische Komposition für schwächere Accounts)

* Andere Armeen können **manuell ergänzt** werden – dies erfordert aber **Codeanpassung**

* Das Skript funktioniert **nicht mit komplexeren Armeen**, da es rein visuell klickt

* Ohne AI nicht perfekt – aber reicht locker, um gemütlich nebenbei Netflix oder Musik zu genießen

---

### Zukünftige Verbesserungen

* KI-Integration (z. B. ChatGPT) zur:

  * **Besseren Loot-Auswertung**
  * **Erkennung von Luftabwehren & Base-Strukturen**
  * **Menschlicheren Angriffen**
* Mehr Konfigurationsoptionen für Armeen und Loot-Grenzwerte

---

### Haftungsausschluss

Dies ist ein **inoffizielles Tool**, steht **nicht in Verbindung mit Supercell**.
Die Nutzung erfolgt **auf eigenes Risiko**. Ein Bann ist theoretisch möglich – auch wenn der Bot „menschlich“ agiert.

---

## English

### Introduction

A fully automated Clash of Clans farming bot that scans loot using OCR and attacks automatically.
A separate tool is included for intentional trophy dropping.

Account names like “MAIN” resp. "1" and “ALT” resp. "2" are **just examples** – feel free to change them in the code.

---

### Features

* OCR-based loot scanning (Tesseract)
* Automated base searching & attacks
* Two account profiles with custom loot requirements
* Optional tool to intentionally lose matches (Trophy Deranker)

---

### System Requirements

* Dual-monitor setup recommended:

  * Monitor 1: Clash of Clans running via Google Play Games (Beta)
  * Monitor 2: For multitasking (e.g. browsing, Netflix)
* Single-monitor setup works too, but the bot will block input during farming
* Windows operating system
* Installed [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/releases/ "Tesseract-OCR GitHub Downloads") (system path, e.g. C:\Program Files\Tesseract-OCR\tesseract.exe)
* Python libraries (install via pip):

```bash
pyautogui cv2 pytesseract numpy Pillow
```

---

### Usage

1. Run `main.py`
2. Select `1` **for MAIN** or `2` **for ALT**
3. The bot will automatically search for a base with sufficient loot
4. Once a good base is found, the attack will start automatically

---

### Trophy Deranker

The **trophy\_deranker.py** script is an **optional extra tool** that intentionally loses matches to drop trophies.
It is ideal for farming in low trophy ranges.

---

### Attack Composition Notes

* **“MAIN” Account**:

  * Troops: E-Dragons, Balloons, Warden, Queen & King
  * Spells: Rage, Zap

* **“ALT” Account**:

  * Troops: Balloons, King
  * Spells: Rage
  * (minimalistic composition for lower-level accounts)

* Other armies can be **manually added** – but this requires **code modification**

* The script **does not work with more complex armies** as it clicks based on visuals

* Without AI, it's not perfect – but it’s good enough for casual Netflix or music while farming

---

### Future Improvements

* AI integration (e.g. ChatGPT) to:

  * **Better loot evaluation**
  * **Air defense & base structure detection**
  * **More human-like attacks**
* More configuration options for troops and loot thresholds

---

### Disclaimer

This is an **unofficial tool** and is **not affiliated with Supercell**.
Use at your own risk. A ban is possible, even though the bot acts "human-like".

