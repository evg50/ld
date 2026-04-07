import subprocess
import sys

DEVICE_ID = sys.argv[1]

def run(cmd):
    return subprocess.getoutput(f"adb -s {DEVICE_ID} {cmd}")

def main():
    devices = subprocess.getoutput("adb devices")
    device_ok = DEVICE_ID in devices

    game_running = "com.readygo.barrel.gp" in run("shell dumpsys activity activities")

    print(f"device: {'online' if device_ok else 'offline'}")
    print(f"game: {'running' if game_running else 'not running'}")

if __name__ == "__main__":
    main()
