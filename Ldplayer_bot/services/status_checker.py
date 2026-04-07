import sys
import threading
import time
import os
from Ldplayer_bot.vision.vision import check_area_xyxy

from Ldplayer_bot.adb_old import take_screenshot

if len(sys.argv) < 2:
    print("❌ Укажи DEVICE_ID при запуске, например: python hunt.py emulator-5556")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

device_id = sys.argv[1]


def watchdog_idle(device_id, screenshot_path, idle_zones, interval=5, threshold=0.7):
    """
    Фоновый watchdog: каждые interval секунд проверяет idle‑статус.
    Если idle найден — печатает предупреждение.
    """
    while True:
        result_idle = check_status(device_id, screenshot_path, idle_zones, threshold)
        if result_idle:
            tpl, action = result_idle
            print(f"⚠️ Watchdog: Idle обнаружен ({tpl} → {action})")
            # здесь можно вызвать restart_hunt(device_id)
        else:
            print("✅ Watchdog: Idle не найден, всё нормально")
        time.sleep(interval)


def start_watchdog_idle(device_id, idle_zones):
    """
    Запускает watchdog_idle в отдельном потоке.
    """
    screenshot_path = os.path.join(BASE_DIR, "screenshots", device_id, "screen.png")
    t = threading.Thread(
        target=watchdog_idle,
        args=(device_id, screenshot_path, idle_zones),
        daemon=True  # поток завершится вместе с программой
    )
    t.start()
    return t

def check_status(device_id, screenshot_path, zones_templates):
    """
    Проверяет наличие хотя бы одного шаблона в каждой зоне.
    zones_templates: список кортежей (area, [templates])
    """
    take_screenshot(device_id)

    for area, templates in zones_templates:
        for tpl in templates:
            tpl_path = os.path.join(BASE_DIR, "templates", "status", tpl)
            if check_area_xyxy(screenshot_path, tpl_path, area, 0.67):
                print(f"✅ Найден шаблон {tpl} в зоне {area}")
                return True
    print("🚫 Ни один шаблон не найден")
    return False

SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", device_id, "screen.png")
# ((512, 531, 535, 538), ["status_z1.png", "status_z2.png", "status_z3.png", "status_z4.png"]),
# ((512, 575, 532, 591), ["status_z1.png", "status_z2.png", "status_z3.png", "status_z4.png"])
zones_templates_idle = [
    ((505, 466, 540, 490), ["status_z1.png", "status_z2.png", "status_z3.png", "status_z4.png"])
   
]

zones_templates_action = [
    ((475, 470, 496, 490), ["status_attack.png", "status_back.png", "status_fight1.png", "status_fight2.png", "status_move.png"])
]

# Основная логика
if check_status(device_id, SCREENSHOT_PATH, zones_templates_idle):
    print("⚡ Статус idle подтверждён")
elif check_status(device_id, SCREENSHOT_PATH, zones_templates_action):
    print("⚡ Статус action подтверждён")
else:
    print("❌ Статус не найден")



result = check_status(device_id, SCREENSHOT_PATH, zones_templates_idle)

if result:
    tpl, action = result
    print(f"⚡ Idle подтверждён — совпал шаблон {tpl}, действие: {action}")
else:
    result = check_status(device_id, SCREENSHOT_PATH, zones_templates_action)
    if result:
        tpl, action = result
        print(f"⚡ Action подтверждён — совпал шаблон {tpl}, действие: {action}")
    else:
        print("❌ Статус не найден")




if __name__ == "__main__":
    # Для теста можно проверить только idle зоны
    result = check_status(device_id, SCREENSHOT_PATH, zones_templates_idle)
    print("Результат проверки idle:", result)
    result = check_status(device_id, SCREENSHOT_PATH, zones_templates_action)
    print("Результат проверки action:", result)
