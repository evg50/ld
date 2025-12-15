import os
from Ldplayer_bot.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE_ID = "emulator-5560"   # подставь свой ID
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")

templates = ("status_z1.png", "status_z2.png", "status_z3.png", "status_z4.png")

def check_status(device_id, screenshot_path, templates, area = (500, 450, 550, 500)):
    take_screenshot(device_id)
    for tpl in templates:
        tpl_path = os.path.join(BASE_DIR, "templates/status", tpl)
        if check_area_xyxy(screenshot_path, tpl_path, area):
            print(f"✅ Найден шаблон: {tpl}")
            return True
    print("🚫 Ни один шаблон не найден")
    return False

if __name__ == "__main__":
    result = check_status(DEVICE_ID, SCREENSHOT_PATH, templates)
    print("Результат проверки:", result)