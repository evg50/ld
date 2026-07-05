# import subprocess
# import sys
# import os
# from datetime import datetime
# ADB = r"H:\LDPlayer\LDPlayer9\adb.exe" 
# DEVICE_ID = sys.argv[1]

# def run(cmd):
#     return subprocess.getoutput(f"adb -s {DEVICE_ID} {cmd}")

# def main():
#     # timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#     # папка для устройства
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     folder = os.path.join(BASE_DIR, "screenshots", DEVICE_ID)
#     os.makedirs(folder, exist_ok=True)

#     # путь сохранения
#     local_path = os.path.join(folder, f"screen_{timestamp}.png")

#     # делаем скриншот
#     run("shell screencap -p /sdcard/screen.png")

#     # скачиваем
#     subprocess.getoutput(f"ADB -s {DEVICE_ID} pull /sdcard/screen.png {local_path}")

#     print(local_path)

# if __name__ == "__main__":
#     main()
#!/usr/bin/env python3
"""
adb_screenshot.py

Скрипт делает скриншот с устройства через adb и сохраняет в папку:
  <project_root>/screenshots/<DEVICE_ID>/screen.png
или в файл с меткой времени (опция).

Usage:
  python adb_screenshot.py <DEVICE_ID> [--timestamp] [--out <path>]

Возвращает путь к сохранённому файлу (печатает в stdout).
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime

# Путь к adb (можно заменить на просто "adb" если adb в PATH)
ADB = r"H:\LDPlayer\LDPlayer9\adb.exe"

def run_adb(device_id: str, args: str) -> str:
    cmd = f'"{ADB}" -s {device_id} {args}'
    return subprocess.getoutput(cmd)

def main():
    parser = argparse.ArgumentParser(description="Take screenshot from device via adb")
    parser.add_argument("device_id", help="DEVICE_ID (adb -s <DEVICE_ID>)")
    parser.add_argument("--timestamp", action="store_true", help="Save with timestamped filename instead of screen.png")
    parser.add_argument("--out", "-o", default=None, help="Optional explicit output path")
    args = parser.parse_args()

    device_id = args.device_id

    # project root = parent of parent of this file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = os.path.join(BASE_DIR, "screenshots", device_id)
    os.makedirs(screenshots_dir, exist_ok=True)

    if args.out:
        local_path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
    else:
        if args.timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            local_path = os.path.join(screenshots_dir, f"screen_{timestamp}.png")
        else:
            local_path = os.path.join(screenshots_dir, "screen.png")

    # Делает скриншот на устройстве
    out1 = run_adb(device_id, "shell screencap -p /sdcard/screen.png")
    # Проверка результата не всегда информативна, поэтому продолжаем к pull

    # Скачиваем файл с устройства
    pull_cmd = f'"{ADB}" -s {device_id} pull /sdcard/screen.png "{local_path}"'
    out2 = subprocess.getoutput(pull_cmd)

    # Проверяем, что файл действительно появился
    if not os.path.isfile(local_path):
        print(f"ERROR: failed to pull screenshot. adb output: {out2}", file=sys.stderr)
        sys.exit(2)

    # Удаляем временный файл на устройстве (опционально)
    _ = run_adb(device_id, "shell rm /sdcard/screen.png")

    # Печатаем путь к сохранённому файлу (для использования из других скриптов)
    print(local_path)
    sys.exit(0)

if __name__ == "__main__":
    main()
#0CD52B#0CD52B