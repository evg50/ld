import os
import sys
import time

from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR

# -----------------------------
# STARTUP PARAMETERS
# -----------------------------
if len(sys.argv) < 4:
    print(" Run: python hunt_smart.py emulator-5562 10 120")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
Count_attack = int(sys.argv[2])
Pausa = int(sys.argv[3])

print(f"Working with device: {DEVICE_ID}")
print(f"Number of attacks: {Count_attack}")
print(f"Pause: {Pausa}")

SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")
print("SCREENSHOT_PATH:", SCREENSHOT_PATH)
print("BASE_DIR:", BASE_DIR)

# -----------------------------
# LOGIC
# -----------------------------

def tap_march():
    take_screenshot(DEVICE_ID)

    # 1. Press big frostbane
    tap(DEVICE_ID, 270, 550)
    time.sleep(2)

    take_screenshot(DEVICE_ID)

    # march
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "march.png"), (150, 600, 350, 720)):
        tap(DEVICE_ID, 280, 670)
        return

    # hospital_full
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "hospital_full.png"), (50, 300, 490, 600)):
        tap(DEVICE_ID, 183, 461)
        tap(DEVICE_ID, 185, 545)
        tap(DEVICE_ID, 280, 670)
        return

    # fuel_reload
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "fuel_reload.png"), (150, 600, 350, 720)):
        print("Fuel required")
        tap(DEVICE_ID, 280, 670)
        time.sleep(2)
        take_screenshot(DEVICE_ID)

        # claim
        if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "claim_btn.png"), (345, 300, 460, 500)):
            tap(DEVICE_ID, 400, 470)
            tap_march()
            return

        if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "claim_btn.png"), (345, 435, 460, 370)):
            tap(DEVICE_ID, 400, 340)
            tap_march()
            return

        tap(DEVICE_ID, 400, 590)
        return

    print("Nothing found on march screen")

def hunt_monster():
    print("Searching for search button...")
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "search_button.png"), (3, 740, 60, 800), 0.5):
        tap(DEVICE_ID, 30, 778)
    elif check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "world_btn.png"), (3, 740, 60, 800), 0.5):
        tap(DEVICE_ID, 30, 778)
        print("Search button not found")
        return

    time.sleep(1)
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "frostbane.png"), (150, 550, 300, 700)):
        tap(DEVICE_ID, 206, 640)
        tap(DEVICE_ID, 260, 915)
    else:
        print("Frostbane not found")
        return

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "confirm.png"), (180, 880, 360, 960)):
        tap(DEVICE_ID, 530, 1830)
    else:
        print("Confirmation not found")

    time.sleep(1)
    tap_march()
    print("Troops sent")

def wait_for_rally(duration):
    print(f"Waiting for rally to finish ({duration} sec)...")
    time.sleep(duration)

def main():
    start = time.time()
    attacks = 0

    for i in range(Count_attack):
        print(f"\nCycle {i+1}")
        hunt_monster()
        attacks += 1
        wait_for_rally(Pausa)

    elapsed = int(time.time() - start)
    print("\nStatistics:")
    print(f"Total attacks: {attacks}")
    print(f"Total time: {elapsed//60} min {elapsed%60} sec")

if __name__ == "__main__":
    main()
