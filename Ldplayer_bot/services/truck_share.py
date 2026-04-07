import os
import time

DEVICE_ID = "127.0.0.1:5557"

def tap(x, y, delay=0.5):
    os.system(f"adb -s {DEVICE_ID} shell input tap {x} {y}")
    time.sleep(delay)

def share_truck():
    print("🚚 Обнаружен truck! Отправляем в чат...")

    # 1. Нажать кнопку Share
    tap(700, 1675)  # координаты кнопки Share

    # 2. Выбрать нужный чат
    tap(720, 1100)   # координаты нужного чата

    # 3. Подтвердить отправку
    tap(400, 1150) # кнопка OK / Send

    print("✅ Сообщение отправлено!")

if __name__ == "__main__":
    share_truck()
