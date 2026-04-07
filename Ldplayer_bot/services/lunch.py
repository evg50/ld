import os
import time
import subprocess

GAME_PACKAGE = "com.readygo.barrel.gp"
GAME_ACTIVITY = "com.im30.aps.debug.UnityPlayerActivityCustom"

DEVICE_ID = "emulator-5558"  # можно вынести в конфиг

def run_adb(cmd):
    full_cmd = f"adb -s {DEVICE_ID} {cmd}"
    print(f"▶ {full_cmd}")
    return subprocess.getoutput(full_cmd)

def check_device():
    devices = run_adb("devices")
    return DEVICE_ID in devices

def start_game():
    print("🎮 Запуск cl...")
    run_adb(f"shell am start -n {GAME_PACKAGE}/{GAME_ACTIVITY}")
    time.sleep(3)


def is_game_running():
    output = run_adb("shell dumpsys activity activities")
    return GAME_PACKAGE in output

def main():
    if not check_device():
        print("🚫 Устройство не найдено")
        return

    while True:
        if not is_game_running():
            print("⚡  запущена — стартуем")
            start_game()
        else:
            print("✅  работает")
        time.sleep(10)  # проверка каждые 10 секунд

if __name__ == "__main__":
    main()
