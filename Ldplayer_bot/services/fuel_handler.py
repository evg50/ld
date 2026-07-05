import os
import time
from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR




def handle_fuel_reload(DEVICE_ID, recursion_level, tap_march):
    """
    Обработчик окна пополнения топлива.
    Всё на find_match:
    - fuel_reload.png
    - claim_btn.png (верх)
    - claim_btn.png (низ)
    - use_item_btn.png (fallback)
    """
    SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")
    # === 1. Ищем окно fuel reload ===
    fuel_reload = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/fuel_reload.png"),
        area=(150, 600, 350, 720),   # рассчитано под кнопку 140x40
        threshold=0.85
    )

    if not fuel_reload:
        print("tap_march: nothing found")
        return False

    print("Fuel required")

    # === 2. Тап по кнопке fuel reload (центр уже возвращён) ===
    tap(DEVICE_ID, fuel_reload[0], fuel_reload[1])
    time.sleep(2)
    take_screenshot(DEVICE_ID)

    # === 3. Claim button (верхний) ===
    claim1 = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/claim_btn.png"),
        area=(345, 420, 470, 500),
        threshold=0.85
    )

    if claim1:
        print("Claim button (1) found")
        tap(DEVICE_ID, claim1[0], claim1[1])
        time.sleep(1)
        return tap_march(DEVICE_ID, recursion_level + 1)


    # === 4. Claim button (нижний) ===
    claim2 = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/claim_btn.png"),
        area=(345, 300, 460, 370),
        threshold=0.85
    )

    if claim2:
        print("Claim button (2) found")
        tap(DEVICE_ID, claim2[0], claim2[1])
        time.sleep(1)
        return tap_march(DEVICE_ID, recursion_level + 1)


    # === 5. Fallback: ищем use_item_btn.png ===
    use_item = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/use_item_btn.png"),
        area=(300, 500, 500, 750),   # область под кнопку 140x40
        threshold=0.85
    )
    tap(DEVICE_ID, use_item[0], use_item[1])

    if use_item:
        print("Use item button found")
        tap(DEVICE_ID, use_item[0], use_item[1])
        time.sleep(1)
        return tap_march(DEVICE_ID, recursion_level + 1)

    # === 6. Ничего не нашли ===
    print("Fuel window closed -> march not sent")
    return False
