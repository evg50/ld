import os
from time import sleep   # ← обязательно

def tap(x, y, DEVICE_ID):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")

def take_screenshot(DEVICE_ID):
    # создаём папку для устройства, если её нет
    folder = f"screenshots/{DEVICE_ID}"
    os.makedirs(folder, exist_ok=True)

    # сохраняем скриншот в папку устройства
    os.system(f"adb -s {DEVICE_ID} exec-out screencap -p > {folder}/screen.png")

def tap_refresh(screen_w, screen_h, DEVICE_ID):
    """Клик по кнопке рефреш через относительные координаты"""
    tap(int(screen_w * 0.93), int(screen_h * 0.052), DEVICE_ID)
    sleep(0.5)
