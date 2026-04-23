
import os
import sys
import time

from Ldplayer_bot.vision.vision import check_area_xyxy, find_match
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
from Ldplayer_bot.services.detect_status import detect_status


# ---------------------------------------------------------
# PARAMETERS
# ---------------------------------------------------------
if len(sys.argv) < 4:
    print("Run: python hunt_smart.py emulator-5562 10 120")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
COUNT_ATTACK = int(sys.argv[2])
PAUSE = int(sys.argv[3])

SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

print(f"Device: {DEVICE_ID}")
print(f"Attacks: {COUNT_ATTACK}")
print(f"Pause: {PAUSE}")
print("Screenshot path:", SCREENSHOT_PATH)


# ---------------------------------------------------------
# TAP MARCH (returns True if march sent)
# ---------------------------------------------------------
def tap_march(recursion_level=0):

    # защита от бесконечной рекурсии
    if recursion_level > 3:
        print("Too many recursive tap_march calls — aborting")
        return False

    take_screenshot(DEVICE_ID)

    # нажимаем frostbane
    tap(DEVICE_ID, 270, 550)
    time.sleep(2)
    take_screenshot(DEVICE_ID)

    # ---------------------------------------------------------
    # 1. MARCH BUTTON
    # ---------------------------------------------------------
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/march.png"),
        (150, 600, 350, 720)
    ):

        # ждём idle
        wait_time = 0
        while wait_time < 130:

            status = detect_status(SCREENSHOT_PATH)

            if status == "idle":
                print("Status: idle")

                # проверяем выбран ли отряд
                troop_selected = check_area_xyxy(
                    SCREENSHOT_PATH,
                    os.path.join(BASE_DIR, "templates/status/selected_troop.png"),
                    (460, 460, 480, 475)
                )

                if not troop_selected:
                    print("Troop not selected → selecting...")
                    tap(DEVICE_ID, 500, 500)
                    time.sleep(0.7)
                    take_screenshot(DEVICE_ID)

                print("Marching now")
                tap(DEVICE_ID, 280, 670)
                return True

            print(f"Status {status}, waiting...")
            time.sleep(1)
            wait_time += 1
            take_screenshot(DEVICE_ID)

        print("Idle not detected — aborting march")
        return False

    # ---------------------------------------------------------
    # 2. HOSPITAL FULL
    # ---------------------------------------------------------
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/hospital_full.png"),
        (50, 300, 490, 600)
    ):
        print("Hospital full → healing...")
        tap(DEVICE_ID, 183, 461)
        tap(DEVICE_ID, 185, 545)
        tap(DEVICE_ID, 280, 670)
        return True  # марш отправлен напрямую

    # ---------------------------------------------------------
    # 3. FUEL RELOAD
    # ---------------------------------------------------------
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/fuel_reload.png"),
        (150, 600, 350, 720)
    ):
        print("Fuel required")
        tap(DEVICE_ID, 280, 670)
        time.sleep(2)
        take_screenshot(DEVICE_ID)

        # claim button (вариант 1)
        if check_area_xyxy(
            SCREENSHOT_PATH,
            os.path.join(BASE_DIR, "templates/claim_btn.png"),
            (345, 420, 470, 500)
        ):
            print("Claim button (1) found")
            tap(DEVICE_ID, 400, 470)
            time.sleep(1)
            return tap_march(recursion_level + 1)

        # claim button (вариант 2)
        if check_area_xyxy(
            SCREENSHOT_PATH,
            os.path.join(BASE_DIR, "templates/claim_btn.png"),
            (345, 300, 460, 370)
        ):
            print("Claim button (2) found")
            tap(DEVICE_ID, 400, 340)
            time.sleep(1)
            return tap_march(recursion_level + 1)

        print("Fuel window closed — march not sent")
        tap(DEVICE_ID, 400, 590)
        return False

    # ---------------------------------------------------------
    # NOTHING FOUND
    # ---------------------------------------------------------
    print("tap_march: nothing found")
    return False


# ---------------------------------------------------------
# HUNT MONSTER (returns True if march sent)
# ---------------------------------------------------------
def hunt_zombie():
    print("Searching for saga button...")
    take_screenshot(DEVICE_ID)

    # search button saga
    match = find_match(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates/buttons/saga_btn.png"), (0, 500, 60, 800))
    if match is True:
        tap(DEVICE_ID, match )
        time.sleep(2)

    # world button
    elif check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/world_btn.png"),
        (430, 865, 540, 960),
        0.5
    ):
        tap(DEVICE_ID, 490, 920)
        print("Search button not found")
        return False

    # march screen open
    elif check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/march.png"),
        (150, 250, 460, 800),
        0.8
    ):
        tap(DEVICE_ID, 20, 15)
        print("Search button not found")
        return False

    time.sleep(1)
    take_screenshot(DEVICE_ID)

    # frostbane
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/frostbane.png"),
        (150, 550, 300, 700)
    ):
        tap(DEVICE_ID, 206, 640)
        tap(DEVICE_ID, 260, 915)
    else:
        print("Frostbane not found")
        return False

    # confirm
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/confirm.png"),
        (180, 880, 360, 960)
    ):
        tap(DEVICE_ID, 530, 1830)
    else:
        print("Confirm not found")

    time.sleep(1)

    # отправляем марш
    result = tap_march()
    if result:
        print("Troops sent")
        return True

    print("Troops NOT sent")
    return False


# ---------------------------------------------------------
# WAIT FOR RALLY
# ---------------------------------------------------------
def wait_for_rally(duration):
    print(f"Waiting for rally ({duration} sec)...")
    time.sleep(duration)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    start = time.time()
    attacks = 0

    for i in range(COUNT_ATTACK):
        print(f"\nCycle {i+1}")

    # повторять попытки, пока не будет успешный марш
        while True:
            if hunt_monster():
                attacks += 1
                wait_for_rally(PAUSE)
                break   # выходим из while и идём к следующему циклу
            else:
                print("Attack failed → retrying...")
                time.sleep(2)

    elapsed = int(time.time() - start)
    print("\nStatistics:")
    print(f"Total attacks: {attacks}")
    print(f"Total time: {elapsed//60} min {elapsed%60} sec")


if __name__ == "__main__":
    main()
