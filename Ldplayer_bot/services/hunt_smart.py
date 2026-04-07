
import os
import sys
import time

from Ldplayer_bot.vision.vision import check_area_xyxy
from Ldplayer_bot.adb import take_screenshot, tap, BASE_DIR

# -----------------------------
# ПАРАМЕТРЫ ЗАПУСКА
# -----------------------------
if len(sys.argv) < 4:
    print("❌ Запуск: python hunt_smart.py emulator-5562 10 120")
    sys.exit(1)

DEVICE_ID = sys.argv[1]
Count_attack = int(sys.argv[2])
Pausa = int(sys.argv[3])

print(f"Работаем с устройством: {DEVICE_ID}")
print(f"колличество атак: {Count_attack}")
print(f"пауза: {Pausa}")

SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots", DEVICE_ID, "screen.png")
print("SCREENSHOT_PATH:", SCREENSHOT_PATH)
print("BASE_DIR:", BASE_DIR)

# -----------------------------
# ЛОГИКА
# -----------------------------

def tap_march():
    take_screenshot(DEVICE_ID)

    # 1. Нажимаем big frostbane
    tap(270, 550, DEVICE_ID)
    time.sleep(2)

    take_screenshot(DEVICE_ID)

    # march
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "march.png"), (150, 600, 350, 720)):
        tap(280, 670, DEVICE_ID)
        return

    # hospital_full
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "hospital_full.png"), (50, 300, 490, 600)):
        tap(183, 461, DEVICE_ID)
        tap(185, 545, DEVICE_ID)
        tap(280, 670, DEVICE_ID)
        return

    # fuel_reload
    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "fuel_reload.png"), (150, 600, 350, 720)):
        print("🚫 need fuel")
        tap(280, 670, DEVICE_ID)
        time.sleep(2)
        take_screenshot(DEVICE_ID)

        # claim
        if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "claim_btn.png"), (345, 300, 460, 500)):
            tap(400, 470, DEVICE_ID)
            tap_march()
            return

        if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "claim_btn.png"), (345, 435, 460, 370)):
            tap(400, 340, DEVICE_ID)
            tap_march()
            return

        tap(400, 590, DEVICE_ID)
        return

    print("⚠️ Ничего не найдено на экране march")

def hunt_monster():
    print("🔍 Ищем кнопку поиска..")
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "search_button.png"), (3, 740, 60, 800), 0.5):
        tap(30, 778, DEVICE_ID)
    elif check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "world_btn.png"), (3, 740, 60, 800), 0.5):
        tap(30, 778, DEVICE_ID)
        print("🚫 Кнопка поиска не найдена,")
        
        return

    time.sleep(1)
    take_screenshot(DEVICE_ID)

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "frostbane.png"), (150, 550, 300, 700)):
        tap(206, 640, DEVICE_ID)
        tap(260, 915, DEVICE_ID)
    else:
        print("🚫 frostbane не найден")
        return

    if check_area_xyxy(SCREENSHOT_PATH, os.path.join(BASE_DIR, "templates", "confirm.png"), (180, 880, 360, 960)):
        tap(530, 1830, DEVICE_ID)
    else:
        print("🚫 Подтверждение не найдено")

    time.sleep(1)
    tap_march()
    print("🚀 Отряд отправлен!")

def wait_for_rally(duration):
    print(f"⏳ Ждём завершения ралли ({duration} сек)...")
    time.sleep(duration)

def main():
    start = time.time()
    attacks = 0

    for i in range(Count_attack):
        print(f"\n🔁 Цикл {i+1}")
        hunt_monster()
        attacks += 1
        wait_for_rally(Pausa)

    elapsed = int(time.time() - start)
    print("\n📊 Статистика:")
    print(f"✅ Всего атак: {attacks}")
    print(f"🕒 Время работы: {elapsed//60} мин {elapsed%60} сек")

if __name__ == "__main__":
    main()
