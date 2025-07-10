@echo off
chcp 65001 >nul
title Clash of Clans Bot

echo.
echo ========================================
echo    Clash of Clans Bot - Başlatılıyor
echo ========================================
echo.

REM Script'in bulunduğu dizine geç
cd /d "%~dp0"

REM Mevcut dizini göster
echo 📁 Çalışma dizini: %CD%
echo.

REM Python'un kurulu olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo Lütfen Python'u kurun: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python bulundu
python --version

REM Gerekli dosyaların varlığını kontrol et
echo.
echo 📋 Dosya kontrolleri:
if exist "main.py" (
    echo ✅ main.py bulundu
) else (
    echo ❌ main.py dosyası bulunamadı!
    echo Mevcut dosyalar:
    dir /b *.py
    pause
    exit /b 1
)

if exist "requirements.txt" (
    echo ✅ requirements.txt bulundu
) else (
    echo ❌ requirements.txt dosyası bulunamadı!
    pause
    exit /b 1
)

if exist ".env" (
    echo ✅ .env dosyası bulundu
) else (
    echo ⚠️ .env dosyası bulunamadı!
    echo Kurulum scripti çalıştırılıyor...
    python setup.py
    if errorlevel 1 (
        echo ❌ Kurulum başarısız!
        pause
        exit /b 1
    )
)

echo.
echo ✅ Bot başlatılıyor...
echo.
echo ⚠️ Önemli Notlar:
echo - Bot'u yönetici olarak çalıştırın
echo - Clash of Clans açık olmalı
echo - Google Play Oyunları (Beta) kurulu olmalı
echo.
echo Durdurmak için Ctrl+C tuşlayın
echo.

REM Bot'u başlat
python main.py

echo.
echo Bot durduruldu.
pause 