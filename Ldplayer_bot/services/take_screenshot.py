import subprocess
import sys
import os

DEVICE_ID = sys.argv[1]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
SCREENSHOT_PATH = os.path.join(SCREENSHOT_DIR, "screen.png")

def run(cmd):
    return subprocess.getoutput(f"adb -s {DEVICE_ID} {cmd}")

def main():
    # создаём папку, если её нет
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # делаем скриншот во временный файл
    tmp_path = "/sdcard/screen_tmp.png"
    run(f"shell screencap -p {tmp_path}")

    # скачиваем на ПК
    run(f"pull {tmp_path} {SCREENSHOT_PATH}")

    # удаляем временный файл
    run(f"shell rm {tmp_path}")

    print("screenshot_ok")

if __name__ == "__main__":
    main()
