import os
from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot, tap
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))





def new_algorithm_flow(device_id):
    """
    Универсальный алгоритм.
    Все координаты и пути к шаблонам ты вставишь сам.
    Паузы:
        - 2 секунды перед анализом скрина
        - 1 секунда после каждого тапа
    """

    # ---------------------------------------------------------
    # ПЕРЕМЕННЫЕ — ТЫ САМ ВСТАВИШЬ КООРДИНАТЫ И ПУТИ
    # ---------------------------------------------------------

    # 1. Проверка шаблона на первом скрине
    REGION_TEMPLATE = (447, 880, 535, 955)
    TEMPLATE_MAIN = os.path.join(BASE_DIR, "templates", "buttons", "world_btn.png")

    # 2. Проверка красного кружка
    REGION_RED = (38, 78, 64, 104)
    TEMPLATE_RED = os.path.join(BASE_DIR, "templates", "buttons", "red_circle.png")

    # 3. Координаты первого тапа
    TAP_1 = (30, 110)

    # 4. Проверка области №1 на втором скрине
    REGION_CHECK_1 = (433, 170, 514, 240)
    TEMPLATE_1 = os.path.join(BASE_DIR, "templates", "buttons", "vip_chest_btn.png")
    TAP_AFTER_1 = (470, 206)
    
    

    # 5. Проверка области №2 на втором скрине
    REGION_CHECK_2 = (360, 645, 510, 710)
    TEMPLATE_2 = os.path.join(BASE_DIR, "templates", "buttons", "vip_claim_btn.png")
    TAP_AFTER_2 = (440, 680)

    # 6. Финальный тап
    FINAL_TAP = (45, 920)

    # Путь к скриншоту для конкретного девайса
    screenshot_path = os.path.join(BASE_DIR, "screenshots", device_id, "screen.png")

    # ---------------------------------------------------------
    # ЛОГИКА АЛГОРИТМА
    # ---------------------------------------------------------

    # --- Шаг 1: первый скрин ---
    take_screenshot(device_id)
    time.sleep(2)  # пауза перед анализом

    # Проверка шаблона
    # if not check_area_xyxy(screenshot_path, TEMPLATE_MAIN, REGION_TEMPLATE):
    #     print("Main template not found")
    #     return False

    # Проверка красного кружка
    if not check_area_xyxy(screenshot_path, TEMPLATE_RED, REGION_RED):
        print("Red circle not found")
        return False

    # --- Шаг 2: первый тап ---
    tap(device_id, TAP_1[0], TAP_1[1])
    time.sleep(3)
     # пауза перед next btn
    

    # --- Шаг 3: второй скрин ---
    take_screenshot(device_id)
    time.sleep(2)

    # --- Шаг 4: проверка области №1 ---
    if check_area_xyxy(screenshot_path, TEMPLATE_1, REGION_CHECK_1):
        tap(device_id, TAP_AFTER_1[0], TAP_AFTER_1[1])
        time.sleep(2)
        tap (device_id, 0, 0)
        time.sleep(1) 

    # --- Шаг 5: проверка области №2 ---
    if check_area_xyxy(screenshot_path, TEMPLATE_2, REGION_CHECK_2):
        tap(device_id, TAP_AFTER_2[0], TAP_AFTER_2[1])
        time.sleep(2)
        tap (device_id, 0, 0)
        time.sleep(1) 


    # --- Шаг 6: финальный тап ---
    tap(device_id, FINAL_TAP[0], FINAL_TAP[1])
    time.sleep(1)

    return True
 

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m Ldplayer_bot.services.new_algorithm <device_id>")
        sys.exit(1)

    device_id = sys.argv[1]
    print(f"Starting Vip for device: {device_id}")

    result = new_algorithm_flow(device_id)

    if result:
        print("Vip finished successfully")
    else:
        print("Vip failed")
