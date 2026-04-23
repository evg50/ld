import os
from time import sleep

from Ldplayer_bot.adb import take_screenshot, tap
from Ldplayer_bot.vision.vision import find_match


# ============================================================
# ПУТИ
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", "screen.png")

PROMO_DIR = os.path.join(BASE_DIR, "templates", "promos")


# ============================================================
# ШАБЛОНЫ
# ============================================================

# Кнопка "Акции"
PROMO_BUTTON_TEMPLATE = os.path.join(PROMO_DIR, "promo_btn.png")
PROMO_BUTTON_AREA = (475, 110, 530, 175)
# PROMO_BUTTON_AREA = (300, 50, 700, 300)

# Skip Animation
SKIP_ON_TEMPLATE = os.path.join(PROMO_DIR, "skip_on_btn.png")
SKIP_OFF_TEMPLATE = os.path.join(PROMO_DIR, "skip_off_btn.png")
SKIP_AREA = (490, 558, 522, 586)

# Кнопка попыток
ATTEMPT_TEMPLATE = os.path.join(PROMO_DIR, "free_attempts_btn.png")
ATTEMPT_AREA = (100, 810, 230, 840)


# ============================================================
# СПИСОК АКЦИЙ
# ============================================================

PROMOS = {
    "gacha_go": {
        "template": os.path.join(PROMO_DIR, "gacha_go_btn.png"),
        "area": (70, 870, 534, 960),
        "handler": None
    }
}


# ============================================================
# ФУНКЦИИ
# ============================================================

def ensure_skip_animation_enabled(device_id):
    """Включает Skip Animation, если выключено."""
    take_screenshot(device_id)

    # OFF → включаем
    off_match = find_match(SCREENSHOT_PATH, SKIP_OFF_TEMPLATE, SKIP_AREA)
    if off_match:
        cx, cy, _ = off_match
        tap(device_id, cx, cy)
        sleep(1)
        return True

    # ON → всё ок
    on_match = find_match(SCREENSHOT_PATH, SKIP_ON_TEMPLATE, SKIP_AREA)
    if on_match:
        return True

    return False


def check_and_open_promo_button(device_id):
    """Проверяет кнопку акций и нажимает её."""
    take_screenshot(device_id)

    match = find_match(SCREENSHOT_PATH, PROMO_BUTTON_TEMPLATE, PROMO_BUTTON_AREA)

    if match is None:
        print("Promo button NOT FOUND")
        return False

    x1, y1, x2, y2 = match
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    print(f"Promo button FOUND at center: {cx}, {cy}")
    tap(device_id, cx, cy)
    
    return True



def detect_promo(device_id):
    """Определяет, какая акция активна."""
    take_screenshot(device_id)

    for promo_name, promo in PROMOS.items():
        match = find_match(SCREENSHOT_PATH, promo["template"], promo["area"])
        if match:
            return promo_name

    return None


# ============================================================
# ОБРАБОТЧИК GACHA GO
# ============================================================

def handle_gacha_go(device_id):
    """Жмёт кнопку попыток, пока она не исчезнет."""

    # 1. Включаем Skip Animation
    ensure_skip_animation_enabled(device_id)

    # 2. Цикл попыток
    while True:
        take_screenshot(device_id)

        match = find_match(SCREENSHOT_PATH, ATTEMPT_TEMPLATE, ATTEMPT_AREA)
        if not match:
            break  # попытки закончились

        cx, cy, _ = match
        tap(device_id, cx, cy)
        sleep(1)


# Назначаем обработчик
PROMOS["gacha_go"]["handler"] = handle_gacha_go


# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================

def process_promo(device_id):
    # 1. Нажимаем кнопку акций
    if not check_and_open_promo_button(device_id):
        print("DEBUG: promo button not found")
        return

    # 2. Новый скрин и определяем акцию
    promo_name = detect_promo(device_id)

    if promo_name is None:
        print("DEBUG: no promo detected after opening promo window")
        return

    # 3. Запускаем обработчик
    handler = PROMOS[promo_name]["handler"]
    handler(device_id)

