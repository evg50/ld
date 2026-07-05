
import os
import sys
import time

from Ldplayer_bot.vision.vision import check_area_xyxy

from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
# from Ldplayer_bot.services.detect_status import detect_status
from Ldplayer_bot.services.screen_analyzer import find_match
from Ldplayer_bot.services.tap_march import tap_march


# ---------------------------------------------------------9lvl 8150
# ---------------------------------------------------------17lvl 147050-
# ---------------------------------------------------------10lvl 8150
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




def hunt_monster():
    print("Searching for search button...")
    take_screenshot(DEVICE_ID)
    # добавить проверку  єкрана world
    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/search_button.png"),
        (3, 740, 60, 800),
        0.5
    ):
        tap(DEVICE_ID, 30, 778)  #tap search btn
        time.sleep(1)

    elif check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/world_btn.png"),
        (430, 865, 540, 960),
        0.5
    ):
        tap(DEVICE_ID, 490, 920) # world btn
        print("Search button not found")
        return False

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

    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/dino.png"),
        (150, 550, 300, 700)
    ):
        tap(DEVICE_ID, 206, 640) # chose frostbane
        tap(DEVICE_ID, 260, 915) #chose  search
        

        time.sleep(2)
        take_screenshot(DEVICE_ID)
        match = find_match (
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/attack_btn.png"),
        (150, 450, 380, 770))
        if match:
            x, y, score = match
            tap(DEVICE_ID, x, y)
        else:
            print("Attack button not found")
            return False


    else:
        print("Frostbane not found")
        return False

    if check_area_xyxy(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/confirm.png"),
        (180, 880, 360, 960)
    ):
        tap(DEVICE_ID, 530, 1830)
    else:
        print("Confirm not found")

    time.sleep(1)

    result = tap_march(DEVICE_ID)

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

        while True:
            if hunt_monster():
                attacks += 1
                wait_for_rally(PAUSE)
                break
            else:
                print("Attack failed -> retrying...")
                time.sleep(2)

    elapsed = int(time.time() - start)
    print("\nStatistics:")
    print(f"Total attacks: {attacks}")
    print(f"Total time: {elapsed//60} min {elapsed%60} sec")


if __name__ == "__main__":
    main()
