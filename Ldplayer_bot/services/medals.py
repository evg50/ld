# проверка что єто правильний єкрна для єтого проверяем на наличие шаблона по координатам 60 270 140 330 шаблон  todays_medal.png/ если да то проверяем награди
# нужно проверить  шаблонний файл  romb.png  в трех координатах . если в перовой есть . вернть 1 сундук взят . если во второй то 2 сунукда взято , если в 3 то 3 сундука взято координати 
# 106 504 150 530  , 256 504 287 530, 390 504 430 530



import os
from Ldplayer_bot.services.template import check_area_xyxy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def check_medals(screenshot_path):
    """
    Возвращает:
    -1 — экран не тот
     0 — экран тот, но сундуки не взяты
     1 — взят первый сундук
     2 — взято два сундука
     3 — взято три сундука
    """

    # 1. Проверяем, что это правильный экран
    if not check_area_xyxy(
        screenshot_path,
        os.path.join(BASE_DIR, "templates", "todays_medal.png"),
        (60, 270, 140, 330),
        threshold=0.7
    ):
        return -1   # экран не тот

    # 2. Координаты зон для romb.png
    zones = [
        (106, 504, 150, 530),  # сундук 1
        (256, 504, 287, 530),  # сундук 2
        (390, 504, 430, 530),  # сундук 3
    ]

    template = os.path.join(BASE_DIR, "templates", "romb.png")

    # 3. Проверяем каждую зону
    for i, area in enumerate(zones, start=1):
        if check_area_xyxy(screenshot_path, template, area, threshold=0.7):
            return i

    return 0  # экран тот, но сундуков нет
