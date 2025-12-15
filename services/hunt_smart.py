# import os
# import sys
# import time
# from Ldplayer_bot.vision import check_area_xyxy

# from Ldplayer_bot.adb import take_screenshot
# # from adb import take_screenshot

# if len(sys.argv) < 2:
#     print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
#     sys.exit(1)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # путь к Ldplayer_bot
# TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "search_button.png")

# DEVICE_ID = sys.argv[1]
# print(f"Работаем с устройством: {DEVICE_ID}")

# SCREEN_DIR = f"screenshots/{DEVICE_ID}"
# os.makedirs(SCREEN_DIR, exist_ok=True)
# # создаём папку для устройства, если её нет
# folder = os.path.join(BASE_DIR, "screenshots", DEVICE_ID)


# SCREENSHOT_PATH = os.path.join(folder, "screen.png")


# def tap(x, y, delay=2):
#     os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")
#     time.sleep(delay)
    
#     # os.makedirs(folder, exist_ok=True)

#     # сохраняем скриншот в папку устройства
#     # os.system(f"adb -s {DEVICE_ID} exec-out screencap -p > {folder}/screen.png")
#     time.sleep(0.5)

# def hunt_monster():
#     print("🔍 Ищем  кнопку поиска...")
#     take_screenshot(DEVICE_ID)

#      # Поиск: диапазон 7 750 50 800  → (x1, y1, x2, y2)
#     if check_area_xyxy(SCREENSHOT_PATH, TEMPLATE_PATH, (3, 740, 60, 800)):
#         tap(30, 778, delay=1.8)
#     else:
#         print("🚫 Кнопка поиска не найдена")  # Поиск добавить визуальную  проверку кнопки диапазон 7 750  50 800
#         return
    
    
#     # tap(206, 640)     # Монстр добавить визуальную  проверку бумера 160 565 245 672
#     time.sleep(1.0)
#     take_screenshot(DEVICE_ID)

#     if check_area_xyxy(SCREENSHOT_PATH, "templates/boomer.png", (150, 550, 300, 700)):
#         tap(206, 640, delay=1.8)
#     else:
#         print("🚫 бумер не найден")
#         return

#     # tap(530, 1830)    # Подтверждение поиска добавить визуальную  проверку 200 890 335 935 кнопка search

#      # Подтверждение: диапазон 200 890 335 935
#     if check_area_xyxy(SCREENSHOT_PATH, "templates/confirm.png", (180, 880, 360, 960)):
#         tap(530, 1830)
#     else:
#         print("🚫 Подтверждение не найдено")

#     # Экран перерисовывается — обновляем
#     time.sleep(1.0)
#     take_screenshot(DEVICE_ID)


#      # Атака на бумера: укажи точный диапазон (пример) check big boomer
#     if check_area_xyxy(SCREENSHOT_PATH, "templates/big_boomer.png", (220, 120, 340, 260)):
#         tap(270, 550)
#     else:
#         print("🚫 boomer not found")
#         return

#     time.sleep(2)

#      # проверка кнопки march

#     take_screenshot(DEVICE_ID)
#     if check_area_xyxy(SCREENSHOT_PATH, "templates/march.png", (225, 650, 335, 685)):
#         tap(280, 670)
#     else:
#         print("🚫 march not found")
#         return

#     time.sleep(2)

#     # tap(275, 915)     # проверка атаки на бумера добавить визуальную  проверку . в єтот момент скрин перерисовивается
#     # time.sleep(2)

#       # Переход на марш — экран меняется, лучше обновить
#     take_screenshot(DEVICE_ID)
#     tap(270, 550)   # Атака
#     tap(280, 665)   # March

#     print("🚀 Отряд отправлен!")

# def wait_for_rally(duration):
#     print(f"⏳ Ждём завершения ралли ({duration} сек)...")
#     time.sleep(duration)

# def main():
#     start = time.time()
#     for i in range(5):
#         print(f"\n🔁 Цикл {i+1}")
#         hunt_monster()
#         wait_for_rally(100)

#     elapsed = int(time.time() - start)
#     print("\n📊 Статистика:")
#     print(f"✅ Всего атак:{i} ")
#     print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

# if __name__ == "__main__":
#     main()
import os
import sys
import time
from Ldplayer_bot.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # корень Ldplayer_bot
DEVICE_ID = sys.argv[1]
print(f"Работаем с устройством: {DEVICE_ID}")

# путь к скриншоту
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

def tap(x, y, delay=2):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")
    time.sleep(delay)

def hunt_smart(DEVICE_ID):
    # запускаем watchdog для idle
    start_watchdog_idle(DEVICE_ID, zones_templates_idle)

    while True:
        hunt_monster(DEVICE_ID)
        # основной цикл охоты, watchdog работает параллельно

def hunt_monster():
    print("🔍 Ищем кнопку поиска...")
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "search_button.png"), (3, 740, 60, 800)):
        tap(30, 778, delay=1.8)
    else:
        print("🚫 Кнопка поиска не найдена")
        return

    time.sleep(1.0)
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "boomer.png"), (150, 550, 300, 700)):
        tap(206, 640, delay=1.8)
        tap(260, 915, delay=1.8)
    else:
        print("🚫 бумер не найден")
        return

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "confirm.png"), (180, 880, 360, 960)):
        tap(530, 1830)
    else:
        print("🚫 Подтверждение не найдено")

    time.sleep(1.0)
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "big_boomer1.png"), (220, 120, 340, 260)):
        tap(270, 550)
    else:
        print("🚫 boomer not found")
        return

    time.sleep(2)
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "march.png"), (225, 650, 335, 685)):
        tap(280, 670,delay=0.5)
    else:
        print("🚫 march not found")
        return

    # time.sleep(2)
    # take_screenshot(DEVICE_ID)
    # print("🚫 tap attack")
    # tap(270, 550, delay=0.5)   # Атака
    # print("🚫 tap march")

    # tap(280, 665, delay=0.5)   # March

    print("🚀 Отряд отправлен!")

def wait_for_rally(duration):
    print(f"⏳ Ждём завершения ралли ({duration} сек)...")
    time.sleep(duration)

def main():
    start = time.time()
    attacks = 0
    for i in range(5):
        print(f"\n🔁 Цикл {i+1}")
        hunt_monster()
        attacks += 1
        wait_for_rally(100)

    elapsed = int(time.time() - start)
    print("\n📊 Статистика:")
    print(f"✅ Всего атак: {attacks}")
    print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()
