@echo off
adb -s emulator-5560 shell screencap -p /sdcard/screen.png
adb -s emulator-5560 pull /sdcard/screen.png screenshots_5560\screen.png
