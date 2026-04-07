from time import sleep
from Ldplayer_bot.adb_old import tap, tap_refresh

def probe_truck_area():
    y = 1106
    x_points = [280,  350]

    print("🔍 Пробуем область генерации грузовиков...")
    for x in x_points:
        print(f"👆 Клик по точке ({x}, {y})")
        tap(x, y)
        sleep(0.3)

    print("⏳ Ожидание 2 секунды...")
    sleep(2)

    print("🔄 Рефреш экрана")
    tap_refresh()

if __name__ == "__main__":
    while True:
        probe_truck_area()
        sleep(2)  # пауза между циклами
