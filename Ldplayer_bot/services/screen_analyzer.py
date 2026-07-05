
import os
import time
import cv2
import numpy as np
import logging
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
from Ldplayer_bot.vision import  check_area_xyxy

# ---------------------------------------------------------
ZONE_MAIN_BTN = (430, 865, 540, 960)
ZONE_MARCH = (150, 600, 350, 720)
ZONE_TRUCKS = (90, 890, 300, 950)
ZONE_SAGA = (11, 13, 190, 65)

# Пути к шаблонам
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
BTN_DIR = os.path.join(TEMPLATES_DIR, "buttons")

WORLD_BTN = os.path.join(BTN_DIR, "world_btn.png")
HQ_BTN = os.path.join(BTN_DIR, "hq_btn.png")
MARCH_PNG = os.path.join(TEMPLATES_DIR, "march.png")
OTHERS_TRUCKS = os.path.join(BTN_DIR, "others' Trucks_btn.png")
SAGA_SCREEN = os.path.join(TEMPLATES_DIR, "saga_screen.png")

# Поведение повторов при отсутствии скриншота
SCREENSHOT_RETRIES = 2
SCREENSHOT_RETRY_DELAY = 1.0  # сек
# Поиск шаблона (возвращает координаты центра)
# ---------------------------------------------------------
def find_match(screenshot_path, template_path, area=None, threshold=0.7):
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


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# Константы зон (left, top, right, bottom)

def _get_screenshot_path(device_id):
    return os.path.join(BASE_DIR, "screenshots", device_id, "screen.png")

def _log_and_return_none(step, template_path, extra=None):
    logger.error(f"[ERROR] step={step} template={template_path} extra={extra or ''}")
    return None

def recognize_screen(DEVICE_ID, default_threshold: float = 0.7, screenshot_path_override: str = None):
    """
    Определяет экран по набору шаблонов.
    - DEVICE_ID: id устройства (строка)
    - default_threshold: порог по умолчанию для find_match
    - screenshot_path_override: путь к файлу скриншота (используется для тестов)
    Возвращает одну из строк:
      "screen_HQ", "screen_world", "screen_world_march", "screen_truck_plunder", "screen_saga"
    При ошибке возвращает None и логирует ошибку.
    """
    # Получаем путь к скриншоту (тестовый override или стандартный)
    if screenshot_path_override:
        screenshot_path = screenshot_path_override
    else:
        screenshot_path = _get_screenshot_path(DEVICE_ID)

    # Проверяем наличие файла, с повтором если нет
    for attempt in range(1, SCREENSHOT_RETRIES + 1):
        if os.path.isfile(screenshot_path):
            break
        if attempt < SCREENSHOT_RETRIES:
            logger.warning(f"[WARN] screenshot not found ({screenshot_path}), retry in {SCREENSHOT_RETRY_DELAY}s (attempt {attempt})")
            time.sleep(SCREENSHOT_RETRY_DELAY)
        else:
            return _log_and_return_none("screenshot_missing", screenshot_path, extra=f"attempts={SCREENSHOT_RETRIES}")

    # --- Проверки в порядке приоритета ---
    # 1) В зоне ZONE_MAIN_BTN ищем world_btn -> вернуть "screen_HQ" (как в ТЗ)
    try:
        res = find_match(screenshot_path, WORLD_BTN, area=ZONE_MAIN_BTN, threshold=default_threshold)
    except Exception as e:
        return _log_and_return_none("find_match_world_btn", WORLD_BTN, extra=str(e))
    if res:
        cx, cy, score = res
        logger.info(f"[CHECK] world_btn found score={score} -> returning screen_HQ")
        return "screen_HQ"

    # 2) В той же зоне ищем hq_btn -> вернуть "screen_world"
    try:
        res = find_match(screenshot_path, HQ_BTN, area=ZONE_MAIN_BTN, threshold=default_threshold)
    except Exception as e:
        return _log_and_return_none("find_match_hq_btn", HQ_BTN, extra=str(e))
    if res:
        cx, cy, score = res
        logger.info(f"[CHECK] hq_btn found score={score} -> returning screen_world")
        return "screen_world"

    # 3) Проверка march (порог 0.85)
    try:
        res = find_match(screenshot_path, MARCH_PNG, area=ZONE_MARCH, threshold=0.85)
    except Exception as e:
        return _log_and_return_none("find_match_march", MARCH_PNG, extra=str(e))
    if res:
        cx, cy, score = res
        logger.info(f"[CHECK] march found score={score} -> returning screen_world_march")
        return "screen_world_march"

    # 4) Проверка others' Trucks (порог 0.6)
    try:
        res = find_match(screenshot_path, OTHERS_TRUCKS, area=ZONE_TRUCKS, threshold=0.6)
    except Exception as e:
        return _log_and_return_none("find_match_trucks", OTHERS_TRUCKS, extra=str(e))
    if res:
        cx, cy, score = res
        logger.info(f"[CHECK] others' Trucks found score={score} -> returning screen_truck_plunder")
        return "screen_truck_plunder"

    # 5) Проверка saga_screen через check_area_xyxy
    try:
        ok = check_area_xyxy(screenshot_path, SAGA_SCREEN, ZONE_SAGA)

    except Exception as e:
        return _log_and_return_none("check_area_saga", SAGA_SCREEN, extra=str(e))
    logger.info(f"[CHECK] saga_screen -> {ok}")
    if ok:
        return "screen_saga"

    # Ничего не найдено
    logger.info("[INFO] no known screen matched")
    return None


# --- Тестовая утилита: прогон по папке с тестовыми скриншотами ---
def test_recognize_on_folder(device_id_for_path, test_folder="C:\Ldplayer_bot\Ldplayer_bot\screenshots\test"):
    """
    Прогон тестов: берет все файлы в test_folder и вызывает recognize_screen
    с override пути. Возвращает dict {filename: result}.
    device_id_for_path нужен только для совместимости с сигнатурой recognize_screen.
    """
    results = {}
    if not os.path.isdir(test_folder):
        logger.error(f"[TEST] test folder not found: {test_folder}")
        return results

    for fname in sorted(os.listdir(test_folder)):
        fpath = os.path.join(test_folder, fname)
        if not os.path.isfile(fpath):
            continue
        res = recognize_screen(device_id_for_path, screenshot_path_override=fpath)
        logger.info(f"[TEST] {fname} -> {res}")
        results[fname] = res
    return results    