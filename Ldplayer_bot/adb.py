

import os
import subprocess
from time import sleep

ADB = r"H:\LDPlayer\LDPlayer9\adb.exe" 
# Абсолютный путь к корню проекта Ldplayer_bot
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tap(device_id, x, y):
    subprocess.run([ADB, "-s", device_id, "shell", "input", "tap", str(x), str(y)])


# slider("emulator-5560", 480, 480, 60, 480)
def slider(device_id, x1, y1, x2, y2, duration=300):
    """
    Универсальный свайп по экрану Android-эмулятора.

    device_id — строка, например "emulator-5560"
    x1, y1 — начальная точка
    x2, y2 — конечная точка
    duration — длительность свайпа в миллисекундах (по умолчанию 300)
    """

    cmd = [
        ADB, "-s", device_id, "shell",
        "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration)
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def take_screenshot(device_id: str):
    folder = os.path.join(BASE_DIR, "screenshots", device_id)
    os.makedirs(folder, exist_ok=True)

    screenshot_path = os.path.join(folder, "screen.png")

    # 1. Скриншот внутри эмулятора
    
    subprocess.run(
    [ADB, "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

    # 2. Копируем на ПК
    subprocess.run(
        [ADB, "-s", device_id, "pull", "/sdcard/screen.png", screenshot_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return screenshot_path

def tap_refresh(device_id, screen_w, screen_h):
    tap( device_id, int(screen_w * 0.93), int(screen_h * 0.052),)
    sleep(0.5)

