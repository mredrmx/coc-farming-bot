@echo off
chcp 65001 >nul
title Clash of Clans Farming Bot - Telegram Kontrol

echo.
echo ========================================
echo   Clash of Clans Farming Bot
echo   Telegram Kontrol Modu
echo ========================================
echo.

echo 🤖 Telegram bot başlatılıyor...
echo.
echo 📋 Kullanım:
echo   1. Telegram'da botunuza mesaj gönderin
echo   2. /start komutu ile başlayın
echo   3. /start_bot ile farming'i başlatın
echo   4. /stop_bot ile farming'i durdurun
echo.

echo ⚠️  Uyarı: Bu bot sadece eğitim amaçlıdır!
echo    Gerçek hesaplarda kullanım sorumluluğu size aittir.
echo.

python telegram_bot.py

echo.
echo Bot kapatıldı. Çıkmak için herhangi bir tuşa basın...
pause >nul 