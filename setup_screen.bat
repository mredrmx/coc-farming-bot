@echo off
chcp 65001 >nul
title Clash of Clans Bot - Ekran Secimi

echo.
echo ========================================
echo   Clash of Clans Bot - Ekran Secimi
echo ========================================
echo.

echo Bot 2. ekranda calismasi icin ekran secimi yapilacak...
echo.

echo Mevcut secenekler:
echo   1. Ana Ekran (Primary) - Varsayilan
echo   2. Ikinci Ekran (1920x1080) - Yaygin
echo   3. Ikinci Ekran (1366x768) - Laptop
echo   4. Ikinci Ekran (2560x1440) - 2K
echo   5. Ikinci Ekran (3840x2160) - 4K
echo   6. Manuel ekran secimi (Arayuz)
echo.

set /p choice="Hangi secenegi kullanmak istiyorsunuz? (1-6): "

if "%choice%"=="1" goto ana_ekran
if "%choice%"=="2" goto ikinci_ekran_1
if "%choice%"=="3" goto ikinci_ekran_2
if "%choice%"=="4" goto ikinci_ekran_3
if "%choice%"=="5" goto ikinci_ekran_4
if "%choice%"=="6" goto manuel_secim
goto varsayilan

:ana_ekran
echo Ana ekran secildi...
echo {"screen_offset_x": 0, "screen_offset_y": 0, "screen_width": 1920, "screen_height": 1080, "screen_name": "Ana Ekran (Primary)"} > screen_config.json
echo Ana ekran ayarlari kaydedildi!
goto son

:ikinci_ekran_1
echo Ikinci ekran (1920x1080) secildi...
echo {"screen_offset_x": 1920, "screen_offset_y": 0, "screen_width": 1920, "screen_height": 1080, "screen_name": "Ikinci Ekran (1920x1080)"} > screen_config.json
echo Ikinci ekran ayarlari kaydedildi!
goto son

:ikinci_ekran_2
echo Ikinci ekran (1366x768) secildi...
echo {"screen_offset_x": 1920, "screen_offset_y": 0, "screen_width": 1366, "screen_height": 768, "screen_name": "Ikinci Ekran (1366x768)"} > screen_config.json
echo Ikinci ekran ayarlari kaydedildi!
goto son

:ikinci_ekran_3
echo Ikinci ekran (2560x1440) secildi...
echo {"screen_offset_x": 1920, "screen_offset_y": 0, "screen_width": 2560, "screen_height": 1440, "screen_name": "Ikinci Ekran (2560x1440)"} > screen_config.json
echo Ikinci ekran ayarlari kaydedildi!
goto son

:ikinci_ekran_4
echo Ikinci ekran (3840x2160) secildi...
echo {"screen_offset_x": 1920, "screen_offset_y": 0, "screen_width": 3840, "screen_height": 2160, "screen_name": "Ikinci Ekran (3840x2160)"} > screen_config.json
echo Ikinci ekran ayarlari kaydedildi!
goto son

:manuel_secim
echo Manuel ekran secimi baslatiliyor...
python screen_setup.py
goto son

:varsayilan
echo Gecersiz secim! Ana ekran kullanilacak.
echo {"screen_offset_x": 0, "screen_offset_y": 0, "screen_width": 1920, "screen_height": 1080, "screen_name": "Ana Ekran (Varsayilan)"} > screen_config.json

:son
echo.
echo screen_config.json dosyasi olusturuldu.
echo.
echo Bot artik secilen ekranda calisacak!
echo.
pause 