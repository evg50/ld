from time import sleep
import subprocess
from adb import take_screenshot, tap, tap_refresh
from vision import find_fragments
import sys
import os
import time

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]

DEVICE_ID = sys.argv[1]
print(f"Работаем с устройством: {DEVICE_ID}")

SCREEN_DIR = f"screenshots/{DEVICE_ID}"
os.makedirs(SCREEN_DIR, exist_ok=True)

SCREENSHOT_PATH = f"screenshots/{DEVICE_ID}/screen.png"


def get_screen_size(device=DEVICE_ID):
    output = subprocess.getoutput(f"adb -s {device} shell wm size")
    size_str = output.split(":")[-1].strip()
    w, h = map(int, size_str.split("x"))
    return w, h

def get_template(screen_w, screen_h):
    if screen_w >= 1080 and screen_h >= 1920:
        return "templates/s_fragment_hd.png"
    else:
        return "templates/s_fragment_ld.png"

def analyze_truck(screen_w, screen_h):
    take_screenshot(DEVICE_ID)
    template = get_template(screen_w, screen_h)
    count = find_fragments(template, SCREENSHOT_PATH)   # возвращает 0,1,2,3
    # print(f"📸 Скриншот сделан, шаблон: {template}")
    # print(f"🔍 Найдено фрагментов: {count}")
    return count

def share_truck(chat_type, screen_w, screen_h):
    tap(int(screen_w*0.65), int(screen_h*0.87), DEVICE_ID)  # Share
    sleep(0.2)
    if chat_type == 1:
        tap(int(screen_w*0.67), int(screen_h*0.56), DEVICE_ID)  # первый чат 2 куска 540
    if chat_type == 3:
        tap(int(screen_w*0.67), int(screen_h*0.56), DEVICE_ID)  # 3 чат 1 кусок  700
    else:
        tap(int(screen_w*0.67), int(screen_h*0.64), DEVICE_ID)  # второй чат (3 куска)  620
    sleep(0.2)
    tap(int(screen_w*0.37), int(screen_h*0.60), DEVICE_ID)  # OK
    sleep(0.5)

def tap_next_truck(screen_w, screen_h, DEVICE_ID):
    tap(int(screen_w*0.88), int(screen_h*0.78), DEVICE_ID)
    sleep(0.5)

def probe_area(screen_w, screen_h):
    y = int(screen_h*0.58)
    for x_ratio in [0.26, 0.32]:
        tap(int(screen_w*x_ratio), y, DEVICE_ID)
        sleep(0.2)

def process_truck(screen_w, screen_h):
    count = analyze_truck(screen_w, screen_h)

    if count == 2:
        now = time.strftime("%Y-%m-%d %H:%M:%S")  # текущее время
        print(f"➡️ [{now}] [{DEVICE_ID}]  чат 1 (2 фрагмента)")
        share_truck(chat_type=1, screen_w=screen_w, screen_h=screen_h)

    # elif count == 2:
    #     print("➡️ Отправляем в чат 1 (2 фрагмента)")
    #     share_truck(chat_type=1, screen_w=screen_w, screen_h=screen_h)

    elif count == 3:
        now = time.strftime("%Y-%m-%d %H:%M:%S")  # текущее время
        print(f"➡️ [{now}] [{DEVICE_ID}]  чат 2 (3 фрагмента)")
        share_truck(chat_type=2, screen_w=screen_w, screen_h=screen_h)

    # else:
        # print("🚫 Грузовик не подходит")


def main():
    screen_w, screen_h = get_screen_size()
    print(f"📱 Экран: {screen_w}x{screen_h}")
    while True:
        # print("🔄 Рефреш экрана")
        tap_refresh(screen_w, screen_h, DEVICE_ID)
        sleep(1)
        # print("📍 Кликаем по области генерации")
        probe_area(screen_w, screen_h)
        sleep(0.5)
        for i in range(12):
            # print(f"\n🚚 Грузовик #{i+1}")
            process_truck(screen_w, screen_h)
            tap_next_truck(screen_w, screen_h, DEVICE_ID)

if __name__ == "__main__":
    main()
