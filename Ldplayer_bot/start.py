# from adb import take_screenshot, tap, tap_refresh
# from vision import find_trucks, find_fragments

# take_screenshot()
# tap()
import subprocess

subprocess.run(["adb", "-s", "emulator-5562", "shell", "screencap", "-p", "/sdcard/test.png"])
subprocess.run(["adb", "-s", "emulator-5562", "pull", "/sdcard/test.png", "test.png"])