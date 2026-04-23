import cv2
import numpy as np
from time import sleep
import os

def to_rect(x1, y1, x2, y2):
    return min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)

def find_fragments(template_path, screenshot_path="screenshots/screen.png",
                   threshold=0.8, output_path="screenshots/matched_slots.png"):
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
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if screenshot is None:
        print("ERROR: screenshot not loaded:", screenshot_path)
        return None

    if template is None:
        print("ERROR: template not loaded:", template_path)
        return None

    x1, y1, x2, y2 = area

    # Проверка границ
    h, w = screenshot.shape[:2]
    if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
        print("ERROR: ROI out of bounds:", area, "screenshot size:", (w, h))
        return None

    roi = screenshot[y1:y2, x1:x2]

    # Проверка пустого ROI
    if roi.size == 0:
        print("ERROR: ROI is empty:", area)
        return None

    # Проверка совпадения каналов
    if roi.ndim != template.ndim:
        print("ERROR: channel mismatch: roi", roi.shape, "template", template.shape)
        return None

    result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        h, w = template.shape[:2]
        return (x1 + top_left[0], y1 + top_left[1],
                x1 + top_left[0] + w, y1 + top_left[1] + h)

    return None


def check_server(
    screenshot_path="screenshots/screen.png",
    server_template="templates/servers/332_2.png",
    server_range=(222, 640, 248, 652),
    threshold=0.7
):
    # Загружаем изображения
    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(server_template)

    if img is None or tmpl is None:
        print("❌ Ошибка загрузки скриншота/шаблона сервера")
        return False

    # Вырезаем область сервера
    x1, y1, x2, y2 = server_range
    crop = img[y1:y2, x1:x2]

    # Сравниваем через matchTemplate
    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    print(f"🔎 Проверка сервера: score={max_val:.3f}, loc={max_loc}")
    return max_val >= threshold

# def check_area_xyxy(screenshot_path, template_path, xyxy, threshold=0.77):
def check_area_xyxy(screenshot_path, template_path, xyxy=(0, 0, 540, 960), threshold=0.77):
    """
    xyxy = (x1, y1, x2, y2)
    Проверяет, совпадает ли шаблон с областью на скриншоте.
    """
    x1, y1, x2, y2 = map(int, xyxy)
    x_min, x_max, y_min, y_max = to_rect(x1, y1, x2, y2)

    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(template_path)

    if img is None or tmpl is None:
        print("❌ Ошибка загрузки скриншота или шаблона")
        return False

    crop = img[y_min:y_max, x_min:x_max]

    # Проверка размеров
    if crop.shape[0] < tmpl.shape[0] or crop.shape[1] < tmpl.shape[1]:
        print(f"❌ Шаблон больше области: crop={crop.shape}, tmpl={tmpl.shape}")
        return False

    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)

    if res.size == 0:
        print("❌ matchTemplate вернул пустой результат")
        return False

    _, max_val, _, _ = cv2.minMaxLoc(res)

    # print(f"🔎 score={max_val:.3f} threshold={threshold}")
    return max_val >= threshold

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
    # print(f"🔎 {template_path} @ ({x_min},{y_min},{x_max},{y_max}): score={max_val:.3f}")
    return max_val >= threshold

# def check_server_multi(
#     screenshot_path,
#     server_templates,
#     server_range,
#     threshold
    
# ):
#     if not os.path.exists(screenshot_path):
#         print(f"🚫 Скриншот не найден: {screenshot_path}")
#         return False

#     img = cv2.imread(screenshot_path)
#     if img is None:
#         print("❌ Ошибка загрузки скриншота")
#         return False

#     x1, y1, x2, y2 = server_range
#     crop = img[y1:y2, x1:x2]

#     for tmpl_path in server_templates:
#         if not os.path.exists(tmpl_path):
#             print(f"🚫 Шаблон не найден: {tmpl_path}")
#             continue

#         tmpl = cv2.imread(tmpl_path)
#         if tmpl is None:
#             print(f"❌ Ошибка загрузки шаблона: {tmpl_path}")
#             continue

#         res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
#         _, max_val, _, max_loc = cv2.minMaxLoc(res)
        
#         # print(f"🔎 Проверка {tmpl_path}: score={max_val:.3f}")
#         if max_val >= threshold:
#             # print(f"✅ Совпадение найдено ({tmpl_path})")
#             return True

#     # print("🚫 Совпадений нет")
#     return False
import cv2
import os
import numpy as np

def debug_match(crop, tmpl, res, out_name):
    """Сохраняет картинку с подсветкой совпадения."""
    if not os.path.exists("debug"):
        os.makedirs("debug")

    crop_vis = crop.copy()
    h, w = tmpl.shape[:2]

    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Рисуем рамку
    cv2.rectangle(crop_vis, top_left, bottom_right, (0, 255, 0), 2)

    # Пишем score
    cv2.putText(
        crop_vis,
        f"{max_val:.3f}",
        (top_left[0], top_left[1] - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.imwrite(f"debug/{out_name}.png", crop_vis)


def check_server_multi(
    screenshot_path,
    server_templates,
    server_range=(180, 640, 210, 655),
    threshold=0.95
):
    img = cv2.imread(screenshot_path)
    if img is None:
        print("❌ Ошибка загрузки скриншота")
        return False

    x1, y1, x2, y2 = server_range
    crop = img[y1:y2, x1:x2]
    crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    for tmpl_path in server_templates:
        tmpl = cv2.imread(tmpl_path)
        if tmpl is None:
            print(f"❌ Ошибка загрузки шаблона: {tmpl_path}")
            continue

        tmpl_gray = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)

        # Пропускаем, если шаблон больше области
        if crop_gray.shape[0] < tmpl_gray.shape[0] or crop_gray.shape[1] < tmpl_gray.shape[1]:
            print(f"⚠️ Шаблон {tmpl_path} больше области — пропуск")
            continue

        res = cv2.matchTemplate(crop_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        # print(f"🔎 {tmpl_path}: score={max_val:.3f}")

        # Сохраняем debug-картинку
        name = os.path.basename(tmpl_path).replace(".png", "")
        debug_match(crop, tmpl, res, f"match_{name}")

        if max_val >= threshold:
            return True

    return False
