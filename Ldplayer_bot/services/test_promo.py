import sys
import time
from Ldplayer_bot.services.promo import (
    detect_promo,
    process_promo,
    check_and_open_promo_button
)
from Ldplayer_bot.adb import take_screenshot


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_promo.py DEVICE_ID")
        sys.exit(1)

    device_id = sys.argv[1]

    print(f"Testing promo detection on device: {device_id}")

    # 1. Нажимаем кнопку акций
    print("Step 1: Checking promo button...")
    if not check_and_open_promo_button(device_id):
        print("Promo button NOT FOUND.")
        return

    print("Promo button clicked.")

    # 2. Ждём, чтобы окно успело открыться
    print("Waiting for promo window to open...")
    time.sleep(2.0)

    # 3. Делаем скриншот после задержки
    take_screenshot(device_id)
    screenshot_path = "screenshot.png"
    print("Saved screenshot:", screenshot_path)

    # 4. Определяем акцию по этому скрину
    print("Step 2: Detecting promo...")
    promo_name = detect_promo(screenshot_path)

    print("detect_promo returned:", promo_name)

    if promo_name is None:
        print("No promo detected after opening promo window.")
        return

    print(f"Promo detected: {promo_name}")

    # 5. Запускаем обработчик
    print("Step 3: Processing promo...")
    process_promo(device_id)

    # 6. Финальный скрин
    time.sleep(0.5)
    take_screenshot(device_id)

    print("Promo processing completed.")


if __name__ == "__main__":
    main()
