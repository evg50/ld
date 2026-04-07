
set DEVICE_ID=emulator-5564

:: Формируем метку времени (заменяем пробелы и двоеточия)
set TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%

:: Убираем возможный пробел в часах (например " 9" → "09")
set TIMESTAMP=%TIMESTAMP: =0%

adb -s %DEVICE_ID% shell screencap -p /sdcard/screen.png
adb -s %DEVICE_ID% pull /sdcard/screen.png screenshots\%DEVICE_ID%\screen_%TIMESTAMP%.png

save: screenshots_%DEVICE_ID%\screen_%TIMESTAMP%.png
