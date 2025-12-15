import os
import subprocess
from time import sleep   # ← обязательно

def tap(x, y, DEVICE_ID):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # путь к Ldplayer_bot

# def take_screenshot(DEVICE_ID):
#     print("🚫 make screenshot")
#     # создаём папку для устройства, если её нет
#     folder = f"screenshots/{DEVICE_ID}"
#     os.makedirs(folder, exist_ok=True)

#     # сохраняем скриншот в папку устройства
#     os.system(f"adb -s {DEVICE_ID} exec-out screencap -p > {folder}/screen.png")

def take_screenshot(device_id: str):
    # print(f"📸 Making screenshot for {device_id}")
    
    folder = os.path.join(BASE_DIR, "screenshots", device_id)
    os.makedirs(folder, exist_ok=True)

    screenshot_path = os.path.join(folder, "screen.png")

    with open(screenshot_path, "wb") as f:
        result = subprocess.run(
            ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
            stdout=f,
            stderr=subprocess.PIPE
        )

    if result.returncode != 0:
        print("❌ Ошибка adb:", result.stderr.decode("utf-8"))
    # else:
        # print(f"✅ Скриншот сохранён: {screenshot_path}")

def tap_refresh(screen_w, screen_h, DEVICE_ID):
    """Клик по кнопке рефреш через относительные координаты"""
    tap(int(screen_w * 0.93), int(screen_h * 0.052), DEVICE_ID)
    sleep(0.5)


