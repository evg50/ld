import os
import time

from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
from Ldplayer_bot.services.detect_status import detect_status
from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.services.fuel_handler import handle_fuel_reload
from Ldplayer_bot.vision.vision import check_area_xyxy





def tap_march(DEVICE_ID, recursion_level=0):
    SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")


    if recursion_level > 3:
        print("Too many recursive tap_march calls - aborting")
        return False

    take_screenshot(DEVICE_ID)

    # === 1. Ищем кнопку march через find_match ===
    march_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/march.png"),
        area=(150, 600, 350, 720),
        threshold=0.85
    )

    if march_btn:
        # === 2. Ждём статус idle ===
        wait_time = 0
        while wait_time < 130:

            status = detect_status(SCREENSHOT_PATH)

            if status == "idle":
            
                print("Status: idle")

                # === 3. Проверка selected_troop (НЕ трогаем) ===
                troop_selected = check_area_xyxy(
                    SCREENSHOT_PATH,
                    os.path.join(BASE_DIR, "templates/status/selected_troop.png"),
                    (460, 460, 480, 475)
                )

                if not troop_selected:
                    print("Troop not selected -> selecting...")
                    tap(DEVICE_ID, 500, 500)
                    time.sleep(0.7)
                    take_screenshot(DEVICE_ID)

                # === 4. Тап по march ===
                print("Marching now")
                tap(DEVICE_ID, march_btn[0], march_btn[1])
                return True

            print(f"Status {status}, waiting...")
            time.sleep(1)
            wait_time += 1
            take_screenshot(DEVICE_ID)

        print("Idle not detected - aborting march")
        return False

    # === 5. HOSPITAL FULL (НЕ трогаем, как ты сказал) ===
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/hospital_full.png"),
        (50, 300, 490, 600)
    ):
        print("Hospital full -> healing...")
        tap(DEVICE_ID, 183, 461)
        tap(DEVICE_ID, 185, 545)
        tap(DEVICE_ID, 280, 670)
        return True

    # === 6. FUEL RELOAD (уже вынесен в отдельный файл) ===
    if handle_fuel_reload(DEVICE_ID, recursion_level, tap_march):
        
        return True

    print("tap_march: nothing found")
    return False
