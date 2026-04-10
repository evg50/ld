import subprocess
import time
import re
import os
import cv2
import numpy as np
from Ldplayer_bot.adb import take_screenshot, BASE_DIR
import os


LDPLAYER_PATH = r"H:\LDPlayer\LDPlayer9\ldconsole.exe"
PACKAGE = "com.readygo.barrel.gp"

print(">>> BASE_DIR =", BASE_DIR)
# -----------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -----------------------------

def run_cmd(cmd):
    return subprocess.getoutput(" ".join(cmd))

def load_templates_from_folder(folder):
    """Загружает все PNG шаблоны из папки."""
    templates = []
    for file in os.listdir(folder):
        if file.lower().endswith(".png"):
            templates.append(os.path.join(folder, file))
    return templates

def match_template(image_path, template_path, threshold=0.8):
    """Проверяет, найден ли шаблон на изображении."""
    print("IMAGE:", image_path)
    print("TEMPLATE:", template_path)

    img = cv2.imread(image_path, 0)
    tpl = cv2.imread(template_path, 0)

    if img is None or tpl is None:
        return False

    res = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    return len(loc[0]) > 0

def get_adb_devices():
    """Возвращает список всех ADB устройств."""
    out = subprocess.getoutput("adb devices")
    devices = []
    for line in out.splitlines():
        if "\tdevice" in line:
            devices.append(line.split("\t")[0])
    return devices

def wait_for_any_template(device, folder, timeout=180, threshold=0.8):
    """
    Ждём появления ЛЮБОГО шаблона из папки.
    Например: templates/start_screen/
    """
    print(f" Ждём появления шаблонов в папке: {folder}")

    templates = load_templates_from_folder(folder)
    if not templates:
        print(f" В папке {folder} нет PNG шаблонов")
        return None

    start = time.time()

    for _ in range(timeout):
        screenshot_path = take_screenshot(device)  # твой метод делает screen.png

        for tpl in templates:
            if match_template(screenshot_path, tpl, threshold):
                print(f" Найден шаблон: {tpl}")
                print(f" Полная загрузка игры: {int(time.time() - start)} сек")
                return tpl

        time.sleep(1)

    print(" Ни один шаблон не найден")
    return None


def launch_emulator(index):
    print(f" Запускаем LDPlayer index={index}")
    run_cmd([LDPLAYER_PATH, "launch", "--index", str(index)])


# -----------------------------
# УМНОЕ ОЖИДАНИЕ LDPLAYER 9
# -----------------------------

def wait_for_emulator_adb(timeout=120):
    """
    Ждём появления нового ADB устройства.
    Это единственный надёжный способ для LDPlayer 9.
    """

    print(" Ждём появления ADB устройства...")
    start = time.time()

    before = set(get_adb_devices())

    for _ in range(timeout):
        after = set(get_adb_devices())
        new = after - before

        if new:
            device_id = list(new)[0]
            print(f" Эмулятор готов, ADB устройство: {device_id}")
            print(f" Время загрузки: {int(time.time() - start)} сек")
            return device_id

        time.sleep(1)

    raise TimeoutError(" ADB устройство не появилось")


# -----------------------------
# УПРАВЛЕНИЕ ИГРОЙ
# -----------------------------

def run_adb(device, cmd):
    return subprocess.getoutput(f"adb -s {device} {cmd}")


def is_game_running(device):
    out = run_adb(device, "shell dumpsys activity activities")
    return PACKAGE in out


def start_game(device):
    print(" Запуск игры...")
    run_adb(device, f"shell monkey -p {PACKAGE} 1")


def force_stop(device):
    print(" Принудительное закрытие игры")
    run_adb(device, f"shell am force-stop {PACKAGE}")


def wait_for_game(device, timeout=40):
    print(" Ждём загрузки игры...")
    start = time.time()

    for _ in range(timeout):
        if is_game_running(device):
            print(f" Игра запущена за {int(time.time() - start)} сек")
            return True
        time.sleep(1)

    return False


# -----------------------------
# ГЛАВНАЯ ФУНКЦИЯ
# -----------------------------

def start_emulator_and_game(index=0):
    """
    Универсальный запуск LDPlayer 9:
    1. Запуск эмулятора
    2. Ожидание появления ADB устройства
    3. Запуск игры
    4. Ожидание полной загрузки по шаблонам
    """

    # 1. Запуск эмулятора
    launch_emulator(index)

    # 2. Ждём появления нового ADB устройства
    device_id = wait_for_emulator_adb()

    # 3. Запуск игры (если не запущена)
    if not is_game_running(device_id):
        start_game(device_id)
        time.sleep(2)

    # 4. Ждём появления процесса игры
    wait_for_game(device_id)

    # 5. Ждём появления ЛЮБОГО шаблона из папки templates/start_screen
    wait_for_any_template(
        device=device_id,
        folder=os.path.join(BASE_DIR, "templates", "start_screen")
        # timeout=180,
        # threshold=0.8
    )

    return device_id

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Ошибка: не передан index")
        sys.exit(1)

    try:
        index = int(sys.argv[1])
    except ValueError:
        print("Ошибка: index должен быть числом")
        sys.exit(1)

    print(f" Получен index = {index}")
    device = start_emulator_and_game(index)

    print(f" Готово! Эмулятор запущен, устройство: {device}")