# import os
# import subprocess
# from time import sleep   # ← обязательно

# def tap(x, y, DEVICE_ID):
#     os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # путь к Ldplayer_bot


# def take_screenshot(device_id: str):
#     folder = os.path.join(BASE_DIR, "screenshots", device_id)
#     os.makedirs(folder, exist_ok=True)

#     screenshot_path = os.path.join(folder, "screen.png")

#     # 1. Делаем скриншот внутри эмулятора
#     subprocess.run(
#         ["adb", "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"],
#         shell=False
#     )

#     # 2. Копируем файл на ПК
#     subprocess.run(
#         ["adb", "-s", device_id, "pull", "/sdcard/screen.png", screenshot_path],
#         shell=False
#     )

#     return screenshot_path

# def tap_refresh(screen_w, screen_h, DEVICE_ID):
#     """Клик по кнопке рефреш через относительные координаты"""
#     tap(int(screen_w * 0.93), int(screen_h * 0.052), DEVICE_ID)
#     sleep(0.5)

import os
import subprocess
from time import sleep

# Абсолютный путь к корню проекта Ldplayer_bot
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tap(device_id, x, y):
    subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)])


def take_screenshot(device_id: str):
    folder = os.path.join(BASE_DIR, "screenshots", device_id)
    os.makedirs(folder, exist_ok=True)

    screenshot_path = os.path.join(folder, "screen.png")

    # 1. Скриншот внутри эмулятора
    subprocess.run(
        ["adb", "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 2. Копируем на ПК
    subprocess.run(
        ["adb", "-s", device_id, "pull", "/sdcard/screen.png", screenshot_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return screenshot_path

def tap_refresh(device_id, screen_w, screen_h):
    tap( device_id, int(screen_w * 0.93), int(screen_h * 0.052),)
    sleep(0.5)

