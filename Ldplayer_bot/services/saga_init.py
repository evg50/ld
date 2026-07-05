# C:\Ldplayer_bot\Ldplayer_bot\services\saga_init.py

import os
import sys
import time
import logging

from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot, tap, slider, BASE_DIR
from Ldplayer_bot.services.screen_analyzer  import recognize_screen
PAUSE = 1
SHORT_PAUSE = 2
LONG_PAUSE = 5
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
logging.basicConfig(level=logging.INFO)

def screenshot_path(device_id):
    return os.path.join(BASE_DIR, "screenshots", device_id, "screen.png")


def refresh_screenshot(device_id):
    time.sleep(PAUSE)

    take_screenshot(device_id)
    

    return screenshot_path(device_id)


def tap_center(device_id, match):
    cx, cy = int(match[0]), int(match[1])
    tap(device_id, cx, cy)
    print(f"[TAP] {cx},{cy}")


def fail(name):
    print(f"[ERROR] {name} not found. Abort.")
    sys.exit(1)


def is_saga_screen(device_id):
    screenshot = refresh_screenshot(device_id)
    area = (11, 13, 190, 65)
    template = os.path.join(BASE_DIR, "templates", "saga_screen.png")

    ok = recognize_screen(device_id)
    if ok == "saga_screen":


    # ok = check_area_xyxy(screenshot, template, area)

        print(f"[CHECK] saga_screen -> {ok}")
    
        return bool(ok)


def start_saga(device_id):

    templates = {
        "event": os.path.join(BASE_DIR, "templates", "buttons", "event_btn.png"),
        "survival1": os.path.join(BASE_DIR, "templates", "buttons", "survival_saga_btn1.png"),
        "survival2": os.path.join(BASE_DIR, "templates", "buttons", "survival_saga_btn2.png"),
        "start": os.path.join(BASE_DIR, "templates", "buttons", "start_btn.png"),
        "advance":  os.path.join(BASE_DIR, "templates", "buttons", "advance_btn.png"),
        "advance1": os.path.join(BASE_DIR, "templates", "buttons", "advance_btn1.png"),

        "normal":   os.path.join(BASE_DIR, "templates", "buttons", "normal_btn.png"),
        "normal1":  os.path.join(BASE_DIR, "templates", "buttons", "normal_btn1.png"),
        "lX": os.path.join(BASE_DIR, "templates", "buttons", "lX_btn.png"),
        "challenge": os.path.join(BASE_DIR, "templates", "buttons", "challenge_btn.png"),
        "confirm": os.path.join(BASE_DIR, "templates", "buttons", "confirm_btn.png"),
    }

    # ---------------------------------------------------------
    # Шаг 1 — Event
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)
    match = find_match(screenshot, templates["event"], area=(470, 47, 540, 105))
    if not match:
        fail("event_btn")
    tap_center(device_id, match)

    # ---------------------------------------------------------
    # Шаг 2 — Пауза
    # ---------------------------------------------------------
    time.sleep(SHORT_PAUSE)

    # ---------------------------------------------------------
    # Шаг 2.1 — survival saga кнопка
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)
    

    match1 = find_match(screenshot, templates["survival1"], area=(60, 860, 540, 960))
    match2 = find_match(screenshot, templates["survival2"], area=(60, 860, 540, 960))

    match = match1 if match1 else match2

    if not match:
        fail("survival_saga_btn")

    tap_center(device_id, match)

    # ---------------------------------------------------------
    # Шаг 3 — Start
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)
    

    match = find_match(screenshot, templates["start"], area=(160, 760, 390, 880))
    if not match:
        fail("start_btn")
    tap_center(device_id, match)

    # ---------------------------------------------------------
    # Шаг 4 — Проверка saga_screen
    # ---------------------------------------------------------
    if not is_saga_screen(device_id):
        fail("saga_screen")

    # ---------------------------------------------------------
    # Шаг 5 — Выбор режима
    # ---------------------------------------------------------
    # Шаг 5 — Выбор режима
    if device_id == "5568":

        screenshot = refresh_screenshot(device_id)

        match1 = find_match(screenshot, templates["advance"],  area=(0, 400, 540, 460))
        match2 = find_match(screenshot, templates["advance1"], area=(0, 400, 540, 460))

        match = match1 if match1 else match2

        if not match:
            fail("advance_btn")

        tap_center(device_id, match)


    else:
        screenshot = screenshot_path(device_id)

        match1 = find_match(screenshot, templates["normal"],  area=None)
        match2 = find_match(screenshot, templates["normal1"], area=None)

        match = match1 if match1 else match2

        if not match:
            fail("normal_btn")

        tap_center(device_id, match)


    # ---------------------------------------------------------
    # Шаг 6 — Свайп вверх 40% экрана
    # ---------------------------------------------------------
    start_x = 260
    start_y = 560
    end_x = start_x
    end_y = 110
    time.sleep(SHORT_PAUSE)

    slider(device_id, start_x, start_y, end_x, end_y, duration=300)
    print("[SLIDE] swipe up 40%")

    # ---------------------------------------------------------
    # Шаг 7 — lX_btn
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)
    match = find_match(screenshot, templates["lX"], area=(430, 835, 460, 860))
    if not match:
        fail("lX_btn")
    tap_center(device_id, match)

    # ---------------------------------------------------------
    # Шаг 8 — Проверка saga + challenge
    # ---------------------------------------------------------
    if not is_saga_screen(device_id):
        fail("saga_screen after lX")

    screenshot = refresh_screenshot(device_id)
    match = find_match(screenshot, templates["challenge"], area=(300, 600, 470, 670))
    if not match:
        fail("challenge_btn")
    tap_center(device_id, match)

    # ---------------------------------------------------------
    # Шаг 9 — Confirm (без проверки saga)
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)
    match = find_match(screenshot, templates["confirm"], area=(80, 520, 470, 605))
    if not match:
        fail("confirm_btn")

    time.sleep(LONG_PAUSE)
    tap_center(device_id, match)

    print("[OK] Saga init completed.")

    # ---------------------------------------------------------
    # Шаг 10 — back_btn
    # ---------------------------------------------------------
    screenshot = refresh_screenshot(device_id)

    match = find_match(
        screenshot,
        os.path.join(BASE_DIR, "templates", "buttons", "back_btn.png"),
        area=(0, 870, 80, 960)
    )

    if not match:
        fail("back_btn")

    tap_center(device_id, match)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python saga_init.py <DEVICE_ID>")
        sys.exit(1)

    DEVICE_ID = sys.argv[1]
    start_saga(DEVICE_ID)
