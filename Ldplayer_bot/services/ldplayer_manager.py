import subprocess
import time
import os
import cv2
import numpy as np
import requests
from datetime import datetime

from Ldplayer_bot.adb import take_screenshot, BASE_DIR
from Ldplayer_bot.services.screen_analyzer import reach_game_start

LDPLAYER_PATH = r"H:\LDPlayer\LDPlayer9\ldconsole.exe"
PACKAGE = "com.readygo.barrel.gp"
ADB_PATH = r"H:\LDPlayer\LDPlayer9\adb.exe"

FRONTEND_API = "http://localhost:3000/checkpoint"

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

# -----------------------------
# FRONTEND CHECKPOINTS
# -----------------------------
def send_checkpoint(label, data=None):
    payload = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "label": label,
        "data": data
    }

    try:
        requests.post(FRONTEND_API, json=payload, timeout=1)
    except Exception:
        pass

def log_checkpoint(name, data=None):
    print(f"\n===== CHECKPOINT: {name} =====")
    if data:
        print(data)
    print("================================\n")
    send_checkpoint(name, data)

# -----------------------------
# ADB / LDPLAYER HELPERS
# -----------------------------
def get_device_id_by_index(index):
    return DEVICE_MAP[index]

def run_cmd(cmd):
    full = " ".join(cmd)
    out = subprocess.getoutput(full)
    log_checkpoint("run_cmd", f"CMD: {full}\nOUT:\n{out}")
    return out

def run_adb(device, cmd):
    full = f"{ADB_PATH} -s {device} {cmd}"
    out = subprocess.getoutput(full)
    log_checkpoint("ADB CMD", f"{full}")
    log_checkpoint("ADB OUTPUT", out)
    return out

def launch_emulator(index):
    run_cmd([LDPLAYER_PATH, "launch", "--index", str(index)])
    log_checkpoint("Эмулятор запущен", f"index={index}")
    time.sleep(3)

def wait_for_device_online(device_id, timeout=60):
    log_checkpoint("Waiting for device online", device_id)

    for i in range(timeout):
        out = subprocess.getoutput(f"{ADB_PATH} devices")
        log_checkpoint(f"adb devices (try {i+1})", out)

        if device_id in out and "offline" not in out:
            log_checkpoint("Device is ONLINE", device_id)
            return True

        time.sleep(1)

    raise TimeoutError(f"{device_id} not online")

def is_game_running(device):
    out = run_adb(device, "shell pidof com.readygo.barrel.gp")
    running = bool(out.strip())
    log_checkpoint("Game running check", f"PID={out}, running={running}")
    return running

def start_game(device):
    log_checkpoint("Starting game")
    out = run_adb(device, f"shell monkey -p {PACKAGE} 1")
    log_checkpoint("Monkey output", out)
    time.sleep(3)

def force_stop(device):
    log_checkpoint("Force stop game")
    run_adb(device, f"shell am force-stop {PACKAGE}")
    time.sleep(2)

def restart_game(device):
    log_checkpoint("Restarting game")
    force_stop(device)
    time.sleep(1)
    run_adb(device, f"shell pkill -f {PACKAGE}")
    time.sleep(1)
    start_game(device)

# -----------------------------
# MAIN LOGIC
# -----------------------------
def start_emulator_and_game(index=5):
    device_id = get_device_id_by_index(index)
    log_checkpoint("Using device", device_id)

    launch_emulator(index)
    wait_for_device_online(device_id)

    MAX_ATTEMPTS = 5

    for attempt in range(1, MAX_ATTEMPTS + 1):
        log_checkpoint("Game start attempt", attempt)

        if not is_game_running(device_id):
            log_checkpoint("Game is NOT running — starting")
            start_game(device_id)
        else:
            log_checkpoint("Game IS running")

        log_checkpoint("Calling reach_game_start()")
        ok = reach_game_start(device_id, timeout=120)
        log_checkpoint("Проверка экрана игры", ok)

        if ok:
            log_checkpoint("Game loaded successfully")
            return device_id

        log_checkpoint("Game did NOT load — restarting game")
        restart_game(device_id)
        time.sleep(3)

    raise RuntimeError("Game failed to start after all attempts")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: index not provided")
        sys.exit(1)

    index = int(sys.argv[1])

    try:
        device_id = start_emulator_and_game(index)
        print("OK:", device_id)

    except Exception as e:
        print("Error:", e)
        print("Restarting in 5 seconds...")
        time.sleep(5)

        python = sys.executable
        os.execv(python, [python] + sys.argv)
