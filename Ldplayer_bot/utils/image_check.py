import cv2
import numpy as np

def load_image(path):
    return cv2.imread(path)

def check_area_xyxy(screenshot_path, template_path, area):
    """
    Проверяет наличие шаблона в указанной области скриншота.
    area = (x1, y1, x2, y2)
    """
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if screenshot is None:
        print(f"❌ Скриншот не найден: {screenshot_path}")
        return False

    if template is None:
        print(f"❌ Шаблон не найден: {template_path}")
        return False

    x1, y1, x2, y2 = area
    crop = screenshot[y1:y2, x1:x2]

    res = cv2.matchTemplate(crop, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    return len(loc[0]) > 0
