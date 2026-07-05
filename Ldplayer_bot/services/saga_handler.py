import os
import time

from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.services.tap_march import tap_march


def saga_error(msg):
    print(f"ERROR: {msg}")
    return False


def run_saga(DEVICE_ID, solo=False, raid=False):
    """
    Один запуск саги:
    1. Нажать saga_search_btn
    2. Нажать attack_saga_btn1/2
    3. Вызвать tap_march (он сам ищет march)
    """

    SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

    # ---------------------------------------------------------
    # ШАГ 1 — saga_search_btn
    # ---------------------------------------------------------
    take_screenshot(DEVICE_ID)

    saga_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/saga_search_btn.png"),
        area=(0, 500, 60, 800),
        threshold=0.6
    )

    if not saga_btn:
        return saga_error("saga_search_btn not found")

    tap(DEVICE_ID, saga_btn[0], saga_btn[1])
    time.sleep(2)

    # ---------------------------------------------------------
    # ШАГ 2 — attack_saga_btn1 / attack_saga_btn2
    # ---------------------------------------------------------
    take_screenshot(DEVICE_ID)

    if solo:
        attack_template = "attack_saga_btn1.png"
    elif raid:
        attack_template = "attack_saga_btn2.png"
    else:
        return saga_error("mode not selected (solo/raid)")

    attack_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons", attack_template),
        area=(180, 500, 360, 600),
        threshold=0.7
    )

    if not attack_btn:
        return saga_error("attack_saga_btn not found")

    tap(DEVICE_ID, attack_btn[0], attack_btn[1])
    time.sleep(1)

    # ---------------------------------------------------------
    # ШАГ 3 — tap_march (он сам ищет march)
    # ---------------------------------------------------------
    result = tap_march(DEVICE_ID)

    if not result:
        return saga_error("tap_march failed")
    if solo: 
        time.sleep(25)
    if raid:
        time.sleep(60)
    return True
