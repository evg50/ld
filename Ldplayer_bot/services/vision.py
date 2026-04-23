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
        print("Error loading screenshot or template")
        return 0

    res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    matches = [(x, y) for (x, y) in zip(*loc[::-1])]

    # Slot coordinates
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


def find_match(screenshot_path, template_path, area=None, threshold=0.8):
    """
    Searches for a template in the screenshot or in a specified area.
    Returns (cx, cy, max_val) or None.
    """

    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if screenshot is None or template is None:
        return None

    if area:
        x1, y1, x2, y2 = area
        roi = screenshot[y1:y2, x1:x2]
        offset_x, offset_y = x1, y1
    else:
        roi = screenshot
        offset_x, offset_y = 0, 0

    result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    top_left = max_loc
    h, w = template.shape[:2]

    cx = offset_x + top_left[0] + w // 2
    cy = offset_y + top_left[1] + h // 2

    return (cx, cy, max_val)


def check_server(
    screenshot_path="screenshots/screen.png",
    server_template="templates/servers/332_2.png",
    server_range=(222, 640, 248, 652),
    threshold=0.7
):
    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(server_template)

    if img is None or tmpl is None:
        print("Error loading screenshot or server template")
        return False

    x1, y1, x2, y2 = server_range
    crop = img[y1:y2, x1:x2]

    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    print(f"Server check: score={max_val:.3f}, loc={max_loc}")
    return max_val >= threshold


def check_area_xyxy(screenshot_path, template_path, xyxy, threshold=0.77):
    """
    xyxy = (x1, y1, x2, y2)
    Compares a region of the screenshot with a template.
    """
    x1, y1, x2, y2 = map(int, xyxy)
    x_min, x_max, y_min, y_max = to_rect(x1, y1, x2, y2)

    img = cv2.imread(screenshot_path)
    tmpl = cv2.imread(template_path)
    if img is None or tmpl is None:
        print("Error loading screenshot or template")
        return False

    crop = img[y_min:y_max, x_min:x_max]
    res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    return max_val >= threshold


def debug_match(crop, tmpl, res, out_name):
    """Saves a debug image with highlighted match."""
    if not os.path.exists("debug"):
        os.makedirs("debug")

    crop_vis = crop.copy()
    h, w = tmpl.shape[:2]

    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(crop_vis, top_left, bottom_right, (0, 255, 0), 2)

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
        print("Error loading screenshot")
        return False

    x1, y1, x2, y2 = server_range
    crop = img[y1:y2, x1:x2]
    crop_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    for tmpl_path in server_templates:
        tmpl = cv2.imread(tmpl_path)
        if tmpl is None:
            print(f"Error loading template: {tmpl_path}")
            continue

        tmpl_gray = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)

        if crop_gray.shape[0] < tmpl_gray.shape[0] or crop_gray.shape[1] < tmpl_gray.shape[1]:
            print(f"Template {tmpl_path} is larger than the area, skipping")
            continue

        res = cv2.matchTemplate(crop_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        name = os.path.basename(tmpl_path).replace(".png", "")
        debug_match(crop, tmpl, res, f"match_{name}")

        if max_val >= threshold:
            return True

    return False
