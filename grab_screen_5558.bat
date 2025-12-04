@echo off
adb -s emulator-5558 shell screencap -p /sdcard/screen.png
adb -s emulator-5558 pull /sdcard/screen.png screenshots_5558\screen.png
