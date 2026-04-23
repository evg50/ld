import os
import sys
import time
from time import sleep

# --- Project imports ---
from Ldplayer_bot.adb import take_screenshot, tap, tap_refresh
from Ldplayer_bot.vision import find_fragments, check_server_multi, check_area_xyxy


# -------------------------------
# 1. Argument check
# -------------------------------
if len(sys.argv) < 2:
    print("Specify DEVICE_ID when launching, for example: python truck_cycle.py emulator-5556")
    sys.exit(1)

DEVICE_ID = sys.argv[1]

DEVICE_NAMES = {
    "emulator-5562": "bandera",
    "emulator-5564": "glory--farm",
    "emulator-5558": "ukrop",
    "emulator-5556": "farm glory",
    "emulator-5554": "Glory",
    "emulator-5560": "glory farm"
}

DEVICE_NAME = DEVICE_NAMES.get(DEVICE_ID, DEVICE_ID)
print(f"Working with device: {DEVICE_NAME}")


# -------------------------------
# 2. Paths and directories
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # services/
BASE_DIR = os.path.dirname(BASE_DIR)                   # Ldplayer_bot/
print(f"BASE_DIR {BASE_DIR}")

SCREEN_DIR = os.path.join(BASE_DIR, "screenshots", DEVICE_ID)
os.makedirs(SCREEN_DIR, exist_ok=True)

SCREENSHOT_PATH = os.path.join(SCREEN_DIR, "screen.png")


# -------------------------------
# 3. Settings
# -------------------------------
CHECK_SERVER = False
WORLD = False


# -------------------------------
# 4. Truck analysis logic
# -------------------------------
def analyze_truck():
    """Scans the screen and counts the number of fragments."""
    take_screenshot(DEVICE_ID)

    templates = [
        os.path.join(BASE_DIR, "templates", "s_fragment_ld.png")
    ]

    total = 0
    for tpl in templates:
        count = find_fragments(tpl, SCREENSHOT_PATH)
        total = max(total, count)

    return total


def share_truck(chat_type):
    """Shares the detected truck to a chat."""
    tap(DEVICE_ID, 350, 830)
    sleep(0.2)

    chat_positions = {
        1: (222, 620),
        2: (222, 540),
        3: (222, 460),
        4: (222, 380)
    }

    x, y = chat_positions.get(chat_type, (222, 540))
    tap(DEVICE_ID, x, y)

    sleep(0.2)
    tap(DEVICE_ID, 200, 580)
    sleep(0.5)


def tap_next_truck():
    tap(DEVICE_ID, 480, 760)
    sleep(0.5)


def probe_area():
    """Clicks the truck generation area."""
    y = 195
    for x in [115, 180]:
        tap(DEVICE_ID, x, y)
        sleep(0.2)


# -------------------------------
# 5. Truck screen detection
# -------------------------------
def check_truck_screen():
    template = os.path.join(BASE_DIR, "templates", "text_loot_truck.png")
    area = (25, 20, 350, 65)

    if check_area_xyxy(SCREENSHOT_PATH, template, area):
        return True

    print("Truck screen not detected")
    enter_truck_screen()
    return False


def enter_truck_screen():
    template = os.path.join(BASE_DIR, "templates", "truck_icon.png")

    if check_area_xyxy(SCREENSHOT_PATH, template):
        print("Truck button detected")
        tap(DEVICE_ID, 30, 600)
        sleep(2)
        take_screenshot(DEVICE_ID)
        return check_truck_screen()

    print("Truck button not detected")
    check_back_arrow()


def check_back_arrow():
    template = os.path.join(BASE_DIR, "templates", "back_arrow.png")
    area = (6, 880, 70, 950)

    if check_area_xyxy(SCREENSHOT_PATH, template, area):
        print("Back arrow detected")
        tap(DEVICE_ID, 35, 915)
        sleep(2)
        take_screenshot(DEVICE_ID)
        return enter_truck_screen()

    print("Back arrow not detected")
    return False


# -------------------------------
# 6. Truck processing
# -------------------------------
def process_truck():
    count = analyze_truck()
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    server_templates = [
        os.path.join(BASE_DIR, "templates", "servers", "24_1.png"),
        os.path.join(BASE_DIR, "templates", "servers", "24_2.png")
    ]

    server_range = (185, 637, 210, 655)

    # 2 fragments
    if count == 2:
        if CHECK_SERVER:
            if not check_server_multi(SCREENSHOT_PATH, server_templates, server_range, 0.80):
                return
        print("2 fragments detected")
        share_truck(1)
        return

    # 1 fragment
    if count == 1:
        if CHECK_SERVER:
            if not check_server_multi(SCREENSHOT_PATH, server_templates, server_range, 0.95):
                return
            print("Sending to chat 1 (1 fragment)")
            share_truck(1)
        return

    # 3 fragments
    if count == 3:
        print(f"[{now}] 3 fragments detected → chat 2")
        share_truck(1)
        return


# -------------------------------
# 7. Main loop
# -------------------------------
def main():
    take_screenshot(DEVICE_ID)

    while True:
        check_truck_screen()
        sleep(1)

        probe_area()
        sleep(0.5)

        for _ in range(12):
            process_truck()
            tap_next_truck()

        tap_refresh(DEVICE_ID, 540, 960)


if __name__ == "__main__":
    main()
