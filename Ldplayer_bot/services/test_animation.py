import os
import sys
import time

from Ldplayer_bot.adb import take_screenshot, BASE_DIR
from Ldplayer_bot.services.screen_analyzer import find_match

DEVICE_ID = sys.argv[1]
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

TEMPLATE = os.path.join(BASE_DIR, "templates/buttons/train_assault_btn.png")
AREA = (330, 525, 376, 565)
THRESHOLD = 0.8

def test_animation(iterations=30, delay=0.15):
    print("Starting animation test...")
    success = 0
    fail = 0

    for i in range(iterations):
        take_screenshot(DEVICE_ID)
        match = find_match(SCREENSHOT_PATH, TEMPLATE, AREA, THRESHOLD)

        if match:
            print(f"{i+1}: OK  at {match}")
            success += 1
        else:
            print(f"{i+1}: FAIL")
            fail += 1

        time.sleep(delay)

    print("----- RESULT -----")
    print("Success:", success)
    print("Fail:", fail)
    print("------------------")

    if fail == 0:
        print("Animation stable. One template is enough.")
    else:
        print("Animation detected. Multiple templates recommended (find_any).")


if __name__ == "__main__":
    test_animation()
