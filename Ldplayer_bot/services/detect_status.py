import os
from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEVICE_ID = "emulator-5554"
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

STATUS_TEMPLATES = {
    "idle": [
        "status_z1.png",
        "status_z2.png",
        "status_z3.png",
        "status_z6.png",
        "status_z5.png",
        "status_z4.png"
    ],
    "lazy": [
        "status_lazy.png"
    ],
    "dead": [
        "status_dead.png"
    ],
    "attack": [
        "status_attack.png",
        "status_fight1.png",
        "status_fight3.png",
        "status_fight8.png",
        "status_fight4.png",
        "status_fight5.png",
        "status_fight6.png",
        "status_fight7.png"
    ],
    "moving": [
        "status_move.png"
    ],
    "returning": [
        "status_back.png"
    ],
    "mining": [
        "status_mine.png"
    ], 
    "no_idle": [
        "no_idle1.png",
        "no_idle2.png"
    ]
}



def detect_status(
        screenshot_path,
        area=(470, 450, 540, 510),
        status_templates=STATUS_TEMPLATES
    ):

   

    for status_name, templates in status_templates.items():
        for tpl in templates:
            tpl_path = os.path.join(BASE_DIR, "templates/status", tpl)

            if check_area_xyxy(screenshot_path, tpl_path, area):
                print(f"Status detected: {status_name} (template: {tpl})")
                return status_name

    print("No status detected")
    return "unknown"

if __name__ == "__main__":
    result = detect_status(DEVICE_ID, SCREENSHOT_PATH, STATUS_TEMPLATES)
    print("Detected status:", result)
