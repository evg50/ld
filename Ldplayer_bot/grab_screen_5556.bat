@echo off
adb -s emulator-5556 shell screencap -p /sdcard/screen_grab.png
adb -s emulator-5556 pull /sdcard/screen_grab.png screenshots\emulator-5556\screen_grab.png
