
import os
import sys
import time
from vision import check_area_xyxy, find_match
from adb import take_screenshot

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
print(f"Работаем с устройством: {DEVICE_ID}")

SCREEN_DIR = f"screenshots/{DEVICE_ID}"
os.makedirs(SCREEN_DIR, exist_ok=True)
SCREENSHOT_PATH = f"{SCREEN_DIR}/screen.png"

def tap(x, y, delay=2):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")
    time.sleep(delay)

def tap_area(area, delay=1.8):
    """Клик по центру заданной области"""
    x1, y1, x2, y2 = area
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    tap(cx, cy, delay=delay)

def watch_for_new_buttons(templates, area, check_interval=5):
    """
    Каждые check_interval секунд проверяем область на наличие новых кнопок.
    templates: список кортежей (template_path, description)
    area: координаты области (x1, y1, x2, y2)
    """
    while True:
        take_screenshot(DEVICE_ID)

        for template, desc in templates:
            coords = find_match(SCREENSHOT_PATH, template, area)
            if coords:
                print(f"✅ Новая кнопка {desc} найдена, кликаем по {coords}")
                tap(coords[0], coords[1], delay=1.8)

                # запускаем процесс лечения заново
                heal()
                return  # выходим, чтобы цикл main снова пошёл

        print(f"⏳ Новых кнопок не найдено, ждём {check_interval} сек...")
        time.sleep(check_interval)

def heal():
    # print("🔍 Ищем кнопку лечения внизу...")

    # area = (60, 750, 200, 810)
    take_screenshot(DEVICE_ID)

    # Просто проверить наличие кнопки
    if check_area_xyxy(SCREENSHOT_PATH, "templates/heal_start.png", (60, 750, 200, 810)):
        print("✅ Кнопка найдена")

    # Найти и кликнуть по кнопке
    coords = find_match(SCREENSHOT_PATH, "templates/heal_start.png", (60, 750, 200, 810))
    if coords:
        tap(coords[0], coords[1], delay=1.8)
    else:
        print("🚫 Кнопка не найдена")

    time.sleep(1.0)

    # новый скриншот проверить кнопку синюю <1h
    take_screenshot(DEVICE_ID)
    if check_area_xyxy(SCREENSHOT_PATH, "templates/heal_00.png", (370, 830, 404, 855)):
        tap(415, 835, delay=1.8)
    else:
        print("🚫 button confirm not found")
        return

    time.sleep(1.0)

    # новый скриншот проверить кнопку heal_help
    take_screenshot(DEVICE_ID)
     # Найти и кликнуть по кнопке
    coords = find_match(SCREENSHOT_PATH, "templates/heal_help.png", (60, 750, 200, 810))
    if coords:
        tap(coords[0], coords[1], delay=1.8)
    
    else:
        print("🚫 button confirm not found")
        return

def wait_for_heal(duration):
    print(f"⏳ Ждём завершения лечения ({duration} сек)...")
    time.sleep(duration)

def main():
    start = time.time()
    i = 0
    while True:   # бесконечный цикл
        i += 1
        print(f"\n🔁 Цикл {i}")
        
        # стандартное лечение
        heal()

        # список новых кнопок для отслеживания
        new_buttons = [
            ("templates/soldier_type1.png", "troop 3"),
            ("templates/soldier_type2.png", "troop 2"),
            ("templates/soldier_type3.png", "troop 1"),
        ]

        # сторож: если кнопка появилась → клик и снова heal()
        watch_for_new_buttons(new_buttons, (60, 750, 200, 810), check_interval=2)

        # если кнопки не появились → просто ждём до следующего цикла
        wait_for_heal(100)

        # статистика времени
        elapsed = int(time.time() - start)
        print(f"📊 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()
