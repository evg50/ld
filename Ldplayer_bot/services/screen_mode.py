import cv2
import os
from config import SWITCH_BUTTON_REGION, MATCH_THRESHOLD

def crop_region(img, region):
    x1, y1, x2, y2 = region
    return img[y1:y2, x1:x2]

def match_template_in_region(img, template_path, region, threshold=MATCH_THRESHOLD):
    template = cv2.imread(template_path)
    if template is None:
        print(f"❌ Не удалось загрузить шаблон: {template_path}")
        return False

    cropped = crop_region(img, region)
    result = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val >= threshold

def get_screen_mode():
    img = cv2.imread("screenshots/screen.png")
    if img is None:
        print("❌ Скриншот не найден")
        return "unknown"

    templates = {
        "base_mode": "templates/switch_button/base_mode.png",
        "map_mode": "templates/switch_button/map_mode.png"
    }

    for mode, path in templates.items():
        if match_template_in_region(img, path, SWITCH_BUTTON_REGION):
            return mode

    return "unknown"
