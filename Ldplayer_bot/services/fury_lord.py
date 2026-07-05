import os
import sys
import time

from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.services.detect_status import detect_status
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR


# ---------------------------------------------------------
# PARAMETERS
# ---------------------------------------------------------
if len(sys.argv) < 2:
    print("Run: python fury_lord.py emulator-5562")
    sys.exit(1)

DEVICE_ID = sys.argv[1]

SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

print("Device:", DEVICE_ID)
print("Screenshot path:", SCREENSHOT_PATH)


# ---------------------------------------------------------
# FURY LORD HUNT
# ---------------------------------------------------------
def hunt_furyLord():
    # 1. Проверяем кнопку event_btn
    take_screenshot(DEVICE_ID)
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/event_btn.png"),
        (470, 50, 540, 960)
    ):
        print("Event button found -> opening event")
        tap(DEVICE_ID, 500, 80)
        time.sleep(1)
        take_screenshot(DEVICE_ID)

    # 2. Ищем fury_lord_btn (2 варианта)
    match = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/fury_lord_btn.png"),
        (70, 860, 540, 960), 0.5
    )

    if not match:
        match = find_match(
            SCREENSHOT_PATH,
            os.path.join(BASE_DIR, "templates/buttons/fury_lord_btn2.png"),
            (70, 860, 540, 960),
            0.5
        )

    if not match:
        print("fury_lord_btn or fury_lord_btn2 not found")
        return False

    x, y, score = match
    print("Fury Lord button found at {},{} -> tapping".format(x, y))
    tap(DEVICE_ID, x, y)
    time.sleep(3)
    take_screenshot(DEVICE_ID)

    # 3. Проверяем red_circle
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/red_circle1.png"),
        (340, 780, 375, 811)
    ):
        print("Red circle found -> tapping target")
        tap(DEVICE_ID, 270, 825)
        time.sleep(6)
        take_screenshot(DEVICE_ID)
    else:
        print("red_circle not found")
        # правильная кнопка назад
        tap(DEVICE_ID, 40, 930)
        time.sleep(1)
        return False

    # 4. Ищем кнопку attack_btn2
    match = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/attack_btn2.png"),
        (280, 515, 350, 600)
    )
    if not match:
        print("attack_btn2 not found")
        return False

    x, y, score = match
    print("Attack button found at {},{} -> tapping".format(x, y))
    tap(DEVICE_ID, x, y)
    time.sleep(2)
    take_screenshot(DEVICE_ID)

    # 4.5 Проверяем окно tips1
    print("Checking for tips1 popup...")
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/tips1.png"),
        (50, 280, 540, 960)
    ):
        print("tips1 detected -> searching for cancel_btn")

        match_cancel = find_match(
            SCREENSHOT_PATH,
            os.path.join(BASE_DIR, "templates/buttons/cancel_btn.png"),
            (0, 0, 540, 960)
        )

        if match_cancel:
            cx, cy, score = match_cancel
            print("Cancel button found at {},{} -> tapping".format(cx, cy))
            tap(DEVICE_ID, cx, cy)
            time.sleep(1)
            take_screenshot(DEVICE_ID)
        else:
            print("Cancel button NOT found even though tips1 is present")

    # 5. Ищем march через find_match
    print("Searching for march button...")
    match_march = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/march.png"),
        (150, 600, 350, 720)
    )

    if not match_march:
        print("march button not found")
        return False

    mx, my, score = match_march
    print("March button found at {},{} -> waiting for idle status...".format(mx, my))

    # Ожидание статуса idle
    wait_time = 0
    while wait_time < 15:
        status = detect_status(SCREENSHOT_PATH)
        print("Status detected:", status)

        if status == "idle":
            print("Status idle -> tapping march at {},{}".format(mx, my))
            tap(DEVICE_ID, mx, my)

            time.sleep(1)

            tap(DEVICE_ID, 510, 920)

            print("March sent -> waiting 40 seconds before next cycle")
            time.sleep(40)
            return True

        time.sleep(1)
        wait_time += 1
        take_screenshot(DEVICE_ID)

    # Если idle так и не появился — fallback
    print("Idle not detected -> tapping march anyway at {},{}".format(mx, my))
    tap(DEVICE_ID, mx, my)

    time.sleep(1)

    tap(DEVICE_ID, 504, 927  )

    print("March sent (fallback) -> waiting 60 seconds before next cycle")

    
    time.sleep(60)


    

    return True


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
def main():
    print("")
    print("Starting Fury Lord hunt...")
    print("")
    cycles = 0

    while True:
        result = hunt_furyLord()

        if not result:
            print("")
            print("No more marches -> Fury Lord hunt finished")
            break

        cycles += 1
        print("Cycle {} completed".format(cycles))
        print("")

    print("")
    print("Total successful cycles:", cycles)


if __name__ == "__main__":
    main()
