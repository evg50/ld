import cv2
import numpy as np
from time import sleep

def to_rect(x1, y1, x2, y2):
    return min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)

def find_fragments(template_path, screenshot_path="screenshots/screen.png",
                   threshold=0.7, output_path="screenshots/matched_slots.png"):
    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(template_path)
    if img is None or tmpl is None:
        print("❌ Ошибка загрузки скриншота/шаблона")
        return 0

    res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    matches = [(x, y) for (x, y) in zip(*loc[::-1])]

    # print(f"🔎 Всего совпадений: {len(matches)}")
    for pt in matches:
        score = res[pt[1], pt[0]]
        # print(f"→ Совпадение: {pt}, score={score:.3f}")

    # Твои координаты слотов
    slot1_range = (98, 745, 155, 800)
    slot2_range = (160, 745, 220, 800)
    slot3_range = (225, 745, 285, 800)

    def in_range(pt, rng):
        return rng[0] <= pt[0] <= rng[1] and rng[2] <= pt[1] <= rng[3]

    found1 = any(in_range(pt, slot1_range) for pt in matches)
    found2 = any(in_range(pt, slot2_range) for pt in matches)
    found3 = any(in_range(pt, slot3_range) for pt in matches)


   

    if found3:
        return 3
    elif found2:
        return 2
    elif found1:
        return 1
    else:
        return 0

def find_match(screenshot_path, template_path, area):
    """
    Ищем шаблон в указанной области скриншота.
    Возвращает координаты прямоугольника совпадения (x1, y1, x2, y2) или None.
    """
    # Загружаем изображения
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    # Вырезаем область из скриншота
    x1, y1, x2, y2 = area
    roi = screenshot[y1:y2, x1:x2]

    # Сравниваем шаблон с областью
    result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Порог совпадения
    threshold = 0.8
    if max_val >= threshold:
        # координаты совпадения внутри ROI
        top_left = max_loc
        h, w = template.shape[:2]
        match_x1 = x1 + top_left[0]
        match_y1 = y1 + top_left[1]
        match_x2 = match_x1 + w
        match_y2 = match_y1 + h
        return (match_x1, match_y1, match_x2, match_y2)

    return None

def check_server(screenshot_path="screenshots/screen.png",
                 server_template="templates/server.png",
                 server_range=(400, 600, 200, 250),
                 threshold=0.8):
    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(server_template)
    if img is None or tmpl is None:
        print("❌ Ошибка загрузки скриншота/шаблона сервера")
        return False

    # Вырезаем область сервера
    crop = img[server_range[2]:server_range[3], server_range[0]:server_range[1]]

    # Сравниваем через matchTemplate
    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    print(f"🔎 Проверка сервера: score={max_val:.3f}")
    return max_val >= threshold

def check_area_xyxy(screenshot_path, template_path, xyxy, threshold=0.8):
    """
    xyxy = (x1, y1, x2, y2) — как в твоих комментариях.
    Сравнивает картинку в области с шаблоном.
    """
    x1, y1, x2, y2 = map(int, xyxy)
    x_min, x_max, y_min, y_max = to_rect(x1, y1, x2, y2)

    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(template_path)
    if img is None or tmpl is None:
        print("❌ Ошибка загрузки скриншота/шаблона")
        return False

    crop = img[y_min:y_max, x_min:x_max]
    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    print(f"🔎 {template_path} @ ({x_min},{y_min},{x_max},{y_max}): score={max_val:.3f}")
    return max_val >= threshold