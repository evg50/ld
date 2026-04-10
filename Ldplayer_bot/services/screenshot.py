import subprocess
import sys
import os
from datetime import datetime

DEVICE_ID = sys.argv[1]

def run(cmd):
    return subprocess.getoutput(f"adb -s {DEVICE_ID} {cmd}")

def main():
    # timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # папка для устройства
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(BASE_DIR, "screenshots", DEVICE_ID)
    os.makedirs(folder, exist_ok=True)

    # путь сохранения
    local_path = os.path.join(folder, f"screen_{timestamp}.png")

    # делаем скриншот
    run("shell screencap -p /sdcard/screen.png")

    # скачиваем
    subprocess.getoutput(f"adb -s {DEVICE_ID} pull /sdcard/screen.png {local_path}")

    print(local_path)

if __name__ == "__main__":
    main()
