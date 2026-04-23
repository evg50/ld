import subprocess
import time
import re
import os
import cv2
import numpy as np
from Ldplayer_bot.adb import take_screenshot, BASE_DIR
import os
from Ldplayer_bot.services.screen_analyzer import reach_game_start


LDPLAYER_PATH = r"H:\LDPlayer\LDPlayer9\ldconsole.exe"
PACKAGE = "com.readygo.barrel.gp"
DEVICE_MAP = {
    0: "emulator-5554",
    1: "emulator-5556",
    2: "emulator-5558",
    3: "emulator-5560",
    4: "emulator-5562",
    5: "emulator-5564",
    6: "emulator-5566",
    7: "emulator-5568",
    8: "emulator-5570",
}

def get_device_id_by_index(index):
    return DEVICE_MAP[index]
print(">>> BASE_DIR =", BASE_DIR)
# -----------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# -----------------------------
def wait_for_device_online(device_id, timeout=500):
    print(f"Ждём появления {device_id} в ADB...")

    for _ in range(timeout):
        out = subprocess.getoutput("adb devices")
        if device_id in out and "offline" not in out:
            print(f"{device_id} готов к работе")
            return True
        time.sleep(1)

    raise TimeoutError(f"{device_id} не появился в ADB")
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

# ---------------------------------------------------------
# Запуск LDPlayer по индексу
# ---------------------------------------------------------
def launch_emulator(index):
    print(f"Запускаем LDPlayer index={index}")
    subprocess.Popen([r"C:\LDPlayer\LDPlayer.exe", f"--index={index}"])
    time.sleep(3)
# ---------------------------------------------------------
# Проверка, запущена ли игра
# ---------------------------------------------------------
def is_game_running(device_id, package="com.lastz.survive.shooter"):
    out = subprocess.getoutput(f"adb -s {device_id} shell pidof {package}")
    return out.strip().isdigit()


# ---------------------------------------------------------
# Запуск игры
# ---------------------------------------------------------
def start_game(device_id, package="com.lastz.survive.shooter"):
    print(f"Запускаем игру на {device_id}")
    subprocess.run(["adb", "-s", device_id, "shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"])
    time.sleep(2)

# ---------------------------------------------------------
# Ожидание, пока устройство появится в ADB
# ---------------------------------------------------------
def wait_for_device_online(device_id, timeout=60):
    print(f"Ждём появления {device_id} в ADB...")

    for _ in range(timeout):
        out = subprocess.getoutput("adb devices")
        if device_id in out and "offline" not in out:
            print(f"{device_id} готов к работе")
            return True
        time.sleep(1)

    raise TimeoutError(f"{device_id} не появился в ADB")

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


def wait_for_device_online(device_id, timeout=260):
    for _ in range(timeout):
        out = subprocess.getoutput("adb devices")
        if device_id in out and "offline" not in out:
            return True
        time.sleep(1)
    raise TimeoutError(f"{device_id} не появился в ADB")



def start_emulator_and_game(index=5):
    device_id = get_device_id_by_index(index)
    print(f"Используем device_id: {device_id}")

    launch_emulator(index)

    wait_for_device_online(device_id)

    if not is_game_running(device_id):
        start_game(device_id)

    reach_game_start(device_id)

    return device_id

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Ошибка: не указан index")
        sys.exit(1)

    index = int(sys.argv[1])
    device_id = start_emulator_and_game(index)
    print(f"OK: {device_id}")
