# from time import sleep
# from adb import take_screenshot, tap, tap_refresh
# from vision import find_trucks, find_fragments

# def is_close(pt1, pt2, tolerance=30):
#     return abs(pt1[0] - pt2[0]) <= tolerance and abs(pt1[1] - pt2[1]) <= tolerance

# visited = []

# while True:
#     take_screenshot()
#     trucks = find_trucks()  # ищем все грузовики
#     trucks = [pt for pt in trucks if pt[1] < 1257]

#     for truck in trucks:
#         if any(is_close(truck, v) for v in visited):
#             print(f"⏭ Уже проверяли грузовик рядом с {truck}, пропускаем")
#             continue

#         visited.append(truck)
#         print(f"🚚 Проверяем грузовик в {truck}")
#         tap(*truck)
#         sleep(1)
#         take_screenshot()

#         fragments = find_fragments("templates/s_fragment.png")
#         count = len(fragments)

#         if 3 <= count <= 5:
#             print(f"✅ Грузовик годный: {count} S-фрагмента — останавливаем цикл")
#             exit()
#         else:
#             print(f"🚫 Грузовик не подходит: {count} S-фрагмента")

#     print("🔄 Ни один грузовик не годится — нажимаем рефреш")
#     tap_refresh()
#     sleep(2)
#     visited.clear()
from time import sleep
from adb import take_screenshot, tap, tap_refresh
from vision import find_trucks, find_fragments

def is_close(pt1, pt2, tolerance=30):
    return abs(pt1[0] - pt2[0]) <= tolerance and abs(pt1[1] - pt2[1]) <= tolerance

def share_truck():
    print("📤 Отправляем грузовик в чат...")

    # 1. Нажать кнопку Share
    tap(700, 1675)  # координаты кнопки Share

    sleep(0.7)

    # 2. Выбрать нужный чат
    tap(720, 1100)   # координаты нужного чата

    sleep(0.7)

    # 3. Подтвердить отправку
    tap(400, 1150) # кнопка OK / Send

    sleep(1)
    print("✅ Грузовик отправлен!")

visited = []

while True:
    take_screenshot()
    trucks = find_trucks()  # ищем все грузовики
    trucks = [pt for pt in trucks if pt[1] < 1257]

    for truck in trucks:
        if any(is_close(truck, v) for v in visited):
            print(f"⏭ Уже проверяли грузовик рядом с {truck}, пропускаем")
            continue

        visited.append(truck)
        print(f"🚚 Проверяем грузовик в {truck}")
        tap(*truck)
        sleep(1)
        take_screenshot()

        fragments = find_fragments("templates/s_fragment.png")
        count = len(fragments)

        if 2 <= count <= 5:
            print(f"✅ Грузовик годный: {count} S-фрагмента — отправляем в чат")
            share_truck()
            break  # после шаринга — выходим из цикла грузовиков
        else:
            print(f"🚫 Грузовик не подходит: {count} S-фрагмента")

    print("🔄 Обновляем список — нажимаем рефреш")
    tap_refresh()
    sleep(2)
    