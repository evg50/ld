from time import sleep, time, strftime
from Ldplayer_bot.adb_old import take_screenshot, tap, tap_refresh
from Ldplayer_bot.vision.vision import find_trucks, find_fragments

def is_close(pt1, pt2, tolerance=30):
    return abs(pt1[0] - pt2[0]) <= tolerance and abs(pt1[1] - pt2[1]) <= tolerance

def share_truck():
    print("📤 Отправляем грузовик в чат...")
    tap(700, 1675)  # Share
    sleep(0.7)
    tap(720, 1100)  # Чат
    sleep(0.7)
    tap(400, 1150)  # OK
    sleep(1)
    print("✅ Грузовик отправлен!")

visited = []
truck_checked = 0
refresh_count = 0
start_time = time()
start_str = strftime("%Y-%m-%d %H:%M:%S")

print(f"🚀 Старт: {start_str}")

while True:
    take_screenshot()
    trucks = find_trucks()
    trucks = [pt for pt in trucks if pt[1] < 1257]

    for truck in trucks:
        if any(is_close(truck, v) for v in visited):
            continue

        visited.append(truck)
        truck_checked += 1
        print(f"🚚 Проверяем грузовик в {truck}")
        tap(*truck)
        sleep(1)
        take_screenshot()

        fragments = find_fragments("templates/s_fragment.png")
        count = len(fragments)

        if 2 <= count <= 5:
            print(f"✅ Грузовик годный: {count} S-фрагмента — отправляем в чат")
            share_truck()
            break
        else:
            print(f"🚫 Не подходит: {count} S-фрагмента")

    refresh_count += 1
    print(f"🔄 Рефреш #{refresh_count}")
    tap_refresh()
    sleep(2)
    visited.clear()

    # Пример: остановка после 10 рефрешей
    if refresh_count >= 10:
        break

end_time = time()
duration = end_time - start_time
minutes = int(duration // 60)
seconds = int(duration % 60)

print("\n📊 Статистика:")
print(f"🕒 Время работы: {minutes} мин {seconds} сек")
print(f"🔁 Рефрешей: {refresh_count}")
print(f"🔍 Грузовиков проверено: {truck_checked}")