# from time import sleep
# import subprocess
# from Ldplayer_bot.adb import take_screenshot, tap, tap_refresh
# from vision import find_fragments,  check_server_multi
# from vision import check_area_xyxy
# import sys
# import os
# import time

# if len(sys.argv) < 2:
#     print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
#     sys.exit(1)






# DEVICE_NAMES = { "emulator-5562": "bandera", "emulator-5564": "glory--farm", "emulator-5558": "ukrop", "emulator-5556": "farm glory", "emulator-5554": "Glory", "emulator-5560": "glory farm" } 
# DEVICE_ID = sys.argv[1]
# DEVICE_NAME = DEVICE_NAMES.get(DEVICE_ID, DEVICE_ID)
# print(f"1 Работаем с устройством: {DEVICE_NAME}")

# SCREEN_DIR = f"screenshots/{DEVICE_ID}"
# os.makedirs(SCREEN_DIR, exist_ok=True)

# SCREENSHOT_PATH = f"screenshots/{DEVICE_ID}/screen.png"

# CHECK_SERVER = False
# WORLD = False

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))






# def analyze_truck():
#     take_screenshot(DEVICE_ID)

#     templates = [
        
        
#         "templates/s_fragment_ld.png"    # ← можно добавить ещё
#     ]

#     total_count = 0
#     for tpl in templates:
#         count = find_fragments(tpl, SCREENSHOT_PATH)
#         total_count = max(total_count, count)  # берём лучший результат

#     return total_count


# def share_truck(chat_type):
#     tap(350, 830, DEVICE_ID)  # Share
#     sleep(0.2)
#     if chat_type == 1:
#         tap(222, 620, DEVICE_ID)  # первый чат 2 куска 540
#     elif chat_type == 3:
#         tap(222,460 , DEVICE_ID)  # 3 alliance кусок  700
#     elif chat_type == 4:
#         tap(222,380 , DEVICE_ID)  # 4 чат world кусок  700
#     else:
#         tap(222, 540, DEVICE_ID)  # второй чат (3 куска)  620
#     sleep(0.2)
#     tap(200, 580, DEVICE_ID)  # OK
#     sleep(0.5)

# def tap_next_truck( DEVICE_ID):
#     tap(480, 760, DEVICE_ID)
#     sleep(0.5)

# def probe_area():
#     y = 195
#     for x in [115, 180, ]:
    
#         tap( x, y, DEVICE_ID)
#         sleep(0.2)

# def check_truck_screen():
#     template_path = os.path.join(BASE_DIR, "Ldplayer_bot", "templates", "text_loot_truck.png")
#     area = (25, 20, 350, 65)

#     if check_area_xyxy(SCREENSHOT_PATH, template_path, area):
#         # print(" Екран  знайдено") 
#         return True

#     print("❌ Екран не знайдено")
#     enter_truck_screen()

#     return False

# def enter_truck_screen():
#     template_path = os.path.join(BASE_DIR, "Ldplayer_bot", "templates", "truck_icon.png")

#     if check_area_xyxy(SCREENSHOT_PATH, template_path, ):
#         print(" кнопка  знайдено")
#         tap (30, 600, DEVICE_ID)
#         sleep(2)
#         take_screenshot(DEVICE_ID)
#         check_truck_screen()

#         return True

#     print("❌ кнопка не знайдено")
#     check_back_arrow()

# def check_back_arrow():
#     template_path = os.path.join(BASE_DIR, "Ldplayer_bot", "templates", "back_arrow.png")
#     area = (6, 880, 70, 950)
#     if check_area_xyxy(SCREENSHOT_PATH, template_path, area):
#         print(" arrow знайдено")
#         tap (35, 915, DEVICE_ID)
#         sleep(2)
#         take_screenshot(DEVICE_ID)
#         enter_truck_screen()

#         return True

#     print("❌ arrow не знайдено")
#     return False



# def process_truck():
#     count = analyze_truck()
#     now = time.strftime("%Y-%m-%d %H:%M:%S")

#     server_templates = [
#         "templates/servers/36_1.png",
#         "templates/servers/36_2.png"
#     ]
#     server_range = (185, 637, 210, 655)

#     # --- 2 фрагмента ---
#     if count == 2:
        

#         if CHECK_SERVER:
#             # print("➡️ Проверяем сервер...")
#             if not check_server_multi(
#                 screenshot_path=SCREENSHOT_PATH,
#                 server_templates=server_templates,
#                 server_range=server_range,
#                 threshold=0.80
#             ):
#                 # print("🚫 Сервер не совпал → пропускаем отправку")
#                 return

#         print("➡️ (2 фрагмента)")
#         share_truck(chat_type=1)
#         return

#     # --- 1 фрагмент ---
#     elif count == 1:
#         # print(f"➡️ [{now}] найден 1 фрагмент")

#         if CHECK_SERVER:
#             # print("➡️ Проверяем сервер...")
#             if not check_server_multi(
#                 screenshot_path=SCREENSHOT_PATH,
#                 server_templates=server_templates,
#                 server_range=server_range,
#                 threshold=0.95
#             ):
#                 # print("🚫 Сервер не совпал → пропускаем отправку")
#                 return

        
#         if CHECK_SERVER:
#             print("➡️ Отправляем в чат 1 (1 фрагмент)")
#             share_truck(chat_type=1)
        
#         return

#     # --- 3 фрагмента ---
#     elif count == 3:
#         print(f"➡️ [{now}] найдено 3 фрагмента → отправляем в чат 2")
#         share_truck(chat_type=2)
#         return

#     # --- Ничего не найдено ---
#     # else:
#         # print(f"ℹ️ [{now}] фрагменты не найдены (count={count})")




# def main():
    
#     take_screenshot(DEVICE_ID)

#     while True:
#         # print("🔄 Рефреш экрана")
#         check_truck_screen()
#         sleep(1)
#         # print("📍 Кликаем по области генерации")
#         probe_area()
#         sleep(0.5)
#         for i in range(12):
#             # print(f"\n🚚 Грузовик #{i+1}")
#             process_truck()
#             tap_next_truck( DEVICE_ID)
        
#         tap_refresh(540, 960, DEVICE_ID)
# if __name__ == "__main__":
#     main()
import os
import sys
import time
from time import sleep

# --- Импорты модулей проекта ---
from Ldplayer_bot.adb import take_screenshot, tap, tap_refresh
from Ldplayer_bot.vision import find_fragments, check_server_multi, check_area_xyxy



# -------------------------------
# 1. Проверка аргументов
# -------------------------------
if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python truck_cycle.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]

DEVICE_NAMES = {
    "emulator-5562": "bandera",
    "emulator-5564": "glory--farm",
    "emulator-5558": "ukrop",
    "emulator-5556": "farm glory",
    "emulator-5554": "Glory",
    "emulator-5560": "glory farm"
}

DEVICE_NAME = DEVICE_NAMES.get(DEVICE_ID, DEVICE_ID)
print(f"Работаем с устройством: {DEVICE_NAME}")


# -------------------------------
# 2. Пути и директории
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # services/
BASE_DIR = os.path.dirname(BASE_DIR)                   # Ldplayer_bot/
print(f"BASE_DIR {BASE_DIR}")

SCREEN_DIR = os.path.join(BASE_DIR, "screenshots", DEVICE_ID)
os.makedirs(SCREEN_DIR, exist_ok=True)

SCREENSHOT_PATH = os.path.join(SCREEN_DIR, "screen.png")


# -------------------------------
# 3. Настройки
# -------------------------------
CHECK_SERVER = False
WORLD = False


# -------------------------------
# 4. Логика анализа грузовика
# -------------------------------
def analyze_truck():
    """Сканирует экран и считает количество фрагментов."""
    take_screenshot(DEVICE_ID)

    templates = [
    os.path.join(BASE_DIR,  "templates", "s_fragment_ld.png")
]


    total = 0
    for tpl in templates:
        count = find_fragments(tpl, SCREENSHOT_PATH)
        total = max(total, count)

    return total


def share_truck(chat_type):
    """Отправка найденного грузовика в чат."""
    tap(350, 830, DEVICE_ID)
    sleep(0.2)

    chat_positions = {
        1: (222, 620),
        2: (222, 540),
        3: (222, 460),
        4: (222, 380)
    }

    x, y = chat_positions.get(chat_type, (222, 540))
    tap(x, y, DEVICE_ID)

    sleep(0.2)
    tap(200, 580, DEVICE_ID)
    sleep(0.5)


def tap_next_truck():
    tap(480, 760, DEVICE_ID)
    sleep(0.5)


def probe_area():
    """Клик по области генерации грузовиков."""
    y = 195
    for x in [115, 180]:
        tap(x, y, DEVICE_ID)
        sleep(0.2)


# -------------------------------
# 5. Проверка экрана грузовика
# -------------------------------
def check_truck_screen():
    template = os.path.join(BASE_DIR, "templates", "text_loot_truck.png")
    area = (25, 20, 350, 65)

    if check_area_xyxy(SCREENSHOT_PATH, template, area):
        return True

    print("❌ Экран грузовика не найден")
    enter_truck_screen()
    return False


def enter_truck_screen():
    template = os.path.join(BASE_DIR,  "templates", "truck_icon.png")

    if check_area_xyxy(SCREENSHOT_PATH, template):
        print("Кнопка грузовика найдена")
        tap(30, 600, DEVICE_ID)
        sleep(2)
        take_screenshot(DEVICE_ID)
        return check_truck_screen()

    print("❌ Кнопка грузовика не найдена")
    check_back_arrow()


def check_back_arrow():
    template = os.path.join(BASE_DIR, "templates", "back_arrow.png")
    area = (6, 880, 70, 950)

    if check_area_xyxy(SCREENSHOT_PATH, template, area):
        print("Стрелка назад найдена")
        tap(35, 915, DEVICE_ID)
        sleep(2)
        take_screenshot(DEVICE_ID)
        return enter_truck_screen()

    print("❌ Стрелка назад не найдена")
    return False


# -------------------------------
# 6. Обработка грузовика
# -------------------------------
def process_truck():
    count = analyze_truck()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    server_templates = [
        os.path.join(BASE_DIR,  "templates", "servers", "36_1.png"),
        os.path.join(BASE_DIR,  "templates", "servers", "36_2.png")
]


    server_range = (185, 637, 210, 655)

    # 2 фрагмента
    if count == 2:
        if CHECK_SERVER:
            if not check_server_multi(SCREENSHOT_PATH, server_templates, server_range, 0.80):
                return
        print("➡️ (2 фрагмента)")
        share_truck(1)
        return

    # 1 фрагмент
    if count == 1:
        if CHECK_SERVER:
            if not check_server_multi(SCREENSHOT_PATH, server_templates, server_range, 0.95):
                return
            print("➡️ Отправляем в чат 1 (1 фрагмент)")
            share_truck(1)
        return

    # 3 фрагмента
    if count == 3:
        print(f"➡️ [{now}] найдено 3 фрагмента → чат 2")
        share_truck(2)
        return


# -------------------------------
# 7. Главный цикл
# -------------------------------
def main():
    take_screenshot(DEVICE_ID)

    while True:
        check_truck_screen()
        sleep(1)

        probe_area()
        sleep(0.5)

        for _ in range(12):
            process_truck()
            tap_next_truck()

        tap_refresh(540, 960, DEVICE_ID)


if __name__ == "__main__":
    main()
