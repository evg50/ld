import os
import sys
import time
import subprocess

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
print(f"Работаем с устройством: {DEVICE_ID}")

SCREEN_DIR = f"screenshots/{DEVICE_ID}"
os.makedirs(SCREEN_DIR, exist_ok=True)
SCREENSHOT_PATH = f"{SCREEN_DIR}/screen.png"

# открываем постоянный adb shell
adb_proc = subprocess.Popen(
    ["adb", "-s", DEVICE_ID, "shell"],
    stdin=subprocess.PIPE,
    text=True
)

def tap_fast(x, y, delay=0.1):
    """Клик по координатам через постоянный канал"""
    adb_proc.stdin.write(f"input tap {x} {y}\n")
    adb_proc.stdin.flush()
    if delay > 0.1:
        time.sleep(delay)

def click():
    tap_fast(270, 555)  # быстрый клик

def main():
    start = time.time()
    for i in range(10):
        print(f"\n🔁 Цикл {i+1}")
        click()

    elapsed = int(time.time() - start)
    print("\n📊 Статистика:")
    print(f"✅ Всего атак: {i}")
    print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()

    

    



def main():
    start = time.time()
    for i in range(10):
        print(f"\n🔁 Цикл {i+1}")
        click()
        

    elapsed = int(time.time() - start)
    print("\n📊 Статистика:")
    print(f"✅ Всего атак:{i} ")
    print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()