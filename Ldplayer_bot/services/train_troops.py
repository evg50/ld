import os
import sys
import time

from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR
from Ldplayer_bot.services.screen_analyzer import find_match

DEVICE_ID = sys.argv[1]
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")


def tap_world_btn():
    take_screenshot(DEVICE_ID)
    world_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/world_btn.png"),
        (430, 865, 540, 960),
        0.8
    )
    if not world_btn:
        print("world_btn not found")
        return False

    tap(DEVICE_ID, world_btn[0], world_btn[1])
    time.sleep(2)

    tap(DEVICE_ID, world_btn[0], world_btn[1])
    time.sleep(2)

    return True


def open_military_center():
    take_screenshot(DEVICE_ID)
    mc = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/military_centr.png"),
        (0, 0, 240, 760),
        0.6
    )
    if not mc:
        print("military_centr not found")
        return False

    tap(DEVICE_ID, mc[0], mc[1])
    time.sleep(1)
    return True


def open_troop_menu():
    take_screenshot(DEVICE_ID)
    troop = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/troop_btn.png"),
        (200, 740, 500, 900),
        0.8
    )
    if not troop:
        print("troop_btn not found")
        return False

    tap(DEVICE_ID, troop[0], troop[1])
    time.sleep(1)
    return True


def tap_train_plus():
    take_screenshot(DEVICE_ID)
    train_plus = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/train+.png"),
        (70,370, 470, 830),
        0.8
    )
    if not train_plus:
        print("train+ not found")
        return False

    tap(DEVICE_ID, train_plus[0], train_plus[1])
    time.sleep(3)
    return True


def tap_back_btn():
    take_screenshot(DEVICE_ID)
    back = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/back_btn.png"),
        (0, 895, 120, 960),
        0.8
    )
    if not back:
        print("back_btn not found")
        return False

    tap(DEVICE_ID, back[0], back[1])
    time.sleep(1)
    return True


def train_type(go_area, train_template):
    # go_btn
    take_screenshot(DEVICE_ID)
    go_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/go_btn.png"),
        go_area,
        0.8
    )
    if not go_btn:
        print("go_btn not found in area", go_area)
        return False

    tap(DEVICE_ID, go_btn[0], go_btn[1])
    time.sleep(2)

    # train_type button
    time.sleep(2)
    take_screenshot(DEVICE_ID)
    train_type_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, train_template),
        (330, 525, 376, 565),
        0.8
    )
    if not train_type_btn:
        print("train_type button not found:", train_template)
        return False

    tap(DEVICE_ID, train_type_btn[0], train_type_btn[1])
    time.sleep(1)

    # train_btn or speed_up_btn
    take_screenshot(DEVICE_ID)
    train_btn = find_match(
        SCREENSHOT_PATH,
        os.path.join(BASE_DIR, "templates/buttons/train_btn.png"),
        (300,880, 490, 950),
        0.8
    )

    if train_btn:
        tap(DEVICE_ID, train_btn[0], train_btn[1])
        time.sleep(1)
    else:
        speed_up = find_match(
            SCREENSHOT_PATH,
            os.path.join(BASE_DIR, "templates/buttons/speed_up_btn.png"),
            (310, 880, 490, 940),
            0.8
        )
        if not speed_up:
            print("train_btn and speed_up_btn not found")
            return False

    # back_btn
    if not tap_back_btn():
        return False

    return True


def assault_cycle():
    print("=== ASSAULT CYCLE ===")
    if not tap_world_btn():
        return False
    if not open_military_center():
        return False
    if not open_troop_menu():
        return False
    if not tap_train_plus():
        return False
    if not train_type((340, 264, 465, 330), "templates/buttons/train_assault_btn.png"):
        return False
    return True


def shooter_cycle():
    print("=== SHOOTER CYCLE ===")
    if not tap_world_btn():
        return False
    if not open_military_center():
        return False
    if not open_troop_menu():
        return False
    if not tap_train_plus():
        return False
    if not train_type((340, 400, 465, 460), "templates/buttons/train_shooter_btn.png"):
        return False
    return True


def rider_cycle():
    print("=== RIDER CYCLE ===")
    if not tap_world_btn():
        return False
    if not open_military_center():
        return False
    if not open_troop_menu():
        return False
    if not tap_train_plus():
        return False
    if not train_type((340, 516, 465, 580), "templates/buttons/train_rider_btn.png"):
        return False
    return True


def train_troops():
    if not assault_cycle():
        return False
    if not shooter_cycle():
        return False
    if not rider_cycle():
        return False

    print("All training cycles completed")
    return True


if __name__ == "__main__":
    train_troops()
