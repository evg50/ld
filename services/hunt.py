import os
import sys
import time
# from adb import take_screenshot

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
print(f"Работаем с устройством: {DEVICE_ID}")
 
SCREEN_DIR = f"screenshots/{DEVICE_ID}"
os.makedirs(SCREEN_DIR, exist_ok=True)

SCREENSHOT_PATH = f"screenshots/{DEVICE_ID}/screen.png"

def tap(x, y, delay=1.5):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")
    time.sleep(delay)

# def take_screenshot():
#     os.system(f"adb -s {DEVICE_ID} exec-out screencap -p > screenshots/screen.png")
#     time.sleep(0.5)

def hunt_monster():
    print("🔍 Ищем монстра...")

    tap(30, 778)      # Поиск
    tap(206, 640)     # Монстр
    tap(530, 1830)    # Подтверждение поиска
    tap(275, 915)
    time.sleep(2)

    tap(270, 550)     # Атака
    tap(280, 665)     # March

    print("🚀 Отряд отправлен!")

def wait_for_rally(duration):
    print(f"⏳ Ждём завершения ралли ({duration} сек)...")
    time.sleep(duration)

def main():
    start = time.time()
    for i in range(10):
        print(f"\n🔁 Цикл {i+1}")
        hunt_monster()
        wait_for_rally(120)

    elapsed = int(time.time() - start)
    print("\n📊 Статистика:")
    print(f"✅ Всего атак:{i} ")
    print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()