# import os
# import time
# import cv2
# import numpy as np
# from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR




# # -----------------------------
# # Поиск шаблона (с координатами центра)
# # -----------------------------
# def find_match(screenshot_path, template_path, area=None, threshold=0.8):
#     screenshot = cv2.imread(screenshot_path)
#     template = cv2.imread(template_path)

#     if screenshot is None or template is None:
#         return None

#     # ROI если указана область
#     if area:
#         x1, y1, x2, y2 = area
#         roi = screenshot[y1:y2, x1:x2]
#         offset_x, offset_y = x1, y1
#     else:
#         roi = screenshot
#         offset_x, offset_y = 0, 0

#     result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

#     if max_val < threshold:
#         return None

#     # координаты совпадения
#     top_left = max_loc
#     h, w = template.shape[:2]

#     # центр кнопки
#     cx = offset_x + top_left[0] + w // 2
#     cy = offset_y + top_left[1] + h // 2

#     return (cx, cy, max_val)


# # -----------------------------
# # Поиск экрана (возвращает тип + координаты кнопки)
# # -----------------------------
# def detect_screen(device):
#     screenshot = take_screenshot(device)
#     print("Проверяем экран:", screenshot)

#     screens = {
#         "update": os.path.join(BASE_DIR, "templates", "update"),
#         "close": os.path.join(BASE_DIR, "templates", "close"),
#         "ok": os.path.join(BASE_DIR, "templates", "ok"),
#         "promo": os.path.join(BASE_DIR, "templates", "promo"),
#         "reward": os.path.join(BASE_DIR, "templates", "reward"),
#         "start": os.path.join(BASE_DIR, "templates", "start_screen")
#     }

#     for name, folder in screens.items():
#         print("Проверяем папку:", name, folder)

#         for file in os.listdir(folder):
#             if file.endswith(".png"):
#                 tpl = os.path.join(folder, file)
#                 print(" --> Шаблон:", tpl)

#                 pos = find_match(screenshot, tpl)
#                 print("   Результат:", pos)

#                 if pos:
#                     return name, pos

#     return None, None

# import subprocess

# # def find_game_device(package_name="com.lastz.survive.shooter"):
# #     devices = subprocess.getoutput("adb devices").splitlines()
# #     devices = [d.split()[0] for d in devices if "device" in d and "offline" not in d]

# #     for dev in devices:
# #         out = subprocess.getoutput(f"adb -s {dev} shell pidof {package_name}")
# #         if out.strip().isdigit():
# #             print(f"Игра найдена в эмуляторе: {dev}")
# #             return dev

# #     print("Игра не найдена ни в одном эмуляторе")
# #     return None


# # -----------------------------
# # Реакция на найденный экран
# # -----------------------------
# def handle_screen(device, screen, pos):
#     if screen == "start":
#         print("Главный экран найден — загрузка завершена")
#         return True

#     if pos:
#         x, y, score = pos
#         print(f"Нажимаем кнопку '{screen}' по координатам {x}, {y} (score={score:.2f})")
#         tap(device, x, y)
#         return False

#     return False


# # -----------------------------
# # Главный цикл загрузки игры
# # -----------------------------
# def reach_game_start(device, timeout=180):
#     print("Начинаем обработку экранов...")

#     start = time.time()

#     while time.time() - start < timeout:
#         screen, pos = detect_screen(device)

#         if screen:
#             done = handle_screen(device, screen, pos)
#             if done:
#                 return True

#         time.sleep(1)

#     print("Не удалось дойти до главного экрана")
#     return False
import os
import time
import cv2
import numpy as np
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR


# ---------------------------------------------------------
# Поиск шаблона (возвращает координаты центра)
# ---------------------------------------------------------
def find_match(screenshot_path, template_path, area=None, threshold=0.8):
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if screenshot is None or template is None:
        return None

    # ROI (если указана область)
    if area:
        x1, y1, x2, y2 = area
        roi = screenshot[y1:y2, x1:x2]
        offset_x, offset_y = x1, y1
    else:
        roi = screenshot
        offset_x, offset_y = 0, 0

    result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    h, w = template.shape[:2]
    cx = offset_x + max_loc[0] + w // 2
    cy = offset_y + max_loc[1] + h // 2

    return (cx, cy, max_val)


# ---------------------------------------------------------
# Поиск экрана (возвращает тип + координаты кнопки)
# ---------------------------------------------------------
def detect_screen(device_id):
    screenshot = take_screenshot(device_id)
    print(f"[SCREEN] analyze: {screenshot}")

    screens = {
        "update": os.path.join(BASE_DIR, "templates", "update"),
        "close": os.path.join(BASE_DIR, "templates", "close"),
        "ok": os.path.join(BASE_DIR, "templates", "ok"),
        "promo": os.path.join(BASE_DIR, "templates", "promo"),
        "reward": os.path.join(BASE_DIR, "templates", "reward"),
        "start": os.path.join(BASE_DIR, "templates", "start_screen"),
    }

    for name, folder in screens.items():
        if not os.path.exists(folder):
            print(f"[WARN] folder not exist: {folder}")
            continue

        print(f"CHECK folder: {name}  {folder}")

        for file in os.listdir(folder):
            if not file.endswith(".png"):
                continue

            tpl = os.path.join(folder, file)
            print(f"    template: {tpl}")

            pos = find_match(screenshot, tpl)

            if pos:
                x, y, score = pos
                print(f"[FOUND] {name} @ {x},{y} (score={score:.2f})")
                return name, pos

    return None, None


# ---------------------------------------------------------
# Обработка найденного экрана
# ---------------------------------------------------------
def handle_screen(device_id, screen, pos):
    if screen == "start":
        print("OK main screen reached")
        return True

    if pos:
        x, y, score = pos
        print(f"[TAP] tap '{screen}' @ {x},{y} (score={score:.2f})")
        tap(device_id, x, y)
        return False

    return False


# ---------------------------------------------------------
# Главный цикл загрузки игры
# ---------------------------------------------------------
def reach_game_start(device_id, timeout=180):
    print("[LOAD] start screen analize...")

    start = time.time()

    while time.time() - start < timeout:
        screen, pos = detect_screen(device_id)

        if screen:
            done = handle_screen(device_id, screen, pos)
            if done:
                return True

        time.sleep(1)

    print("[FAIL] main screen dont reached")
    return False