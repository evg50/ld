import os
import sys
import time
import cv2
import numpy as np


# ==========================
# CONFIG
# ==========================

TEMPLATES_PATH = r"C:\Ldplayer_bot\Ldplayer_bot\templates\numbers"

ARENA_ROWS = 5
ROW_HEIGHT = 150
FIRST_ROW_CENTER_Y = 300

POWER_X1 = 210
POWER_X2 = 410
POWER_Y1 = 295
POWER_Y2 = 320

MATCH_THRESHOLD = 0.85


# ==========================
# ADB HELPERS
# ==========================

def adb(cmd: str):
    os.system(cmd)


def adb_screencap(device_id: str, out_path: str):
    tmp_path = "/sdcard/__arena_tmp.png"
    adb(f'adb -s {device_id} shell screencap -p {tmp_path}')
    adb(f'adb -s {device_id} pull {tmp_path} "{out_path}"')
    adb(f'adb -s {device_id} shell rm {tmp_path}')

    if not os.path.exists(out_path):
        return None

    return cv2.imread(out_path)


def tap(device_id: str, x: int, y: int):
    adb(f'adb -s {device_id} shell input tap {x} {y}')


# ==========================
# TEMPLATE LOADING
# ==========================

def load_templates():
    white_tmpl = {}
    red_tmpl = {}
    letter_tmpl = {}

    for fname in os.listdir(TEMPLATES_PATH):
        if not fname.endswith(".png"):
            continue

        path = os.path.join(TEMPLATES_PATH, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        name = fname[:-4]

        if name.isdigit():
            white_tmpl[name] = img
            continue

        if name.endswith("r") and name[:-1].isdigit():
            red_tmpl[name[:-1]] = img
            continue

        letter_tmpl[name] = img

    return white_tmpl, red_tmpl, letter_tmpl


# ==========================
# OCR TEMPLATE MATCHING
# ==========================

def match_symbol(slice_img, templates, threshold=MATCH_THRESHOLD):
    best_char = None
    best_score = 0
    best_width = 0

    for char, tmpl in templates.items():
        th, tw = tmpl.shape[:2]

        if slice_img.shape[1] < tw:
            continue

        region = slice_img[:, :tw]
        res = cv2.matchTemplate(region, tmpl, cv2.TM_CCOEFF_NORMED)
        score = float(res[0][0])

        if score > best_score and score >= threshold:
            best_score = score
            best_char = char
            best_width = tw

    return best_char, best_width


def read_power_number(area, start_x, white_tmpl, red_tmpl, letter_tmpl):
    gray = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

    x = start_x
    h, w = gray.shape[:2]

    digit_gap = 1
    overlap = 2

    result = ""

    while x < w:
        slice_img = gray[:, x:x + 50]

        char, cw = match_symbol(slice_img, white_tmpl)
        if char is None:
            char, cw = match_symbol(slice_img, red_tmpl)

        if char is None:
            x += 1
            continue

        result += char
        x += max(1, cw - overlap + digit_gap)

        if char == "dot":
            break

    while x < w:
        slice_img = gray[:, x:x + 50]

        char, cw = match_symbol(slice_img, letter_tmpl)

        if char in ["K", "M"]:
            result += char
            break

        x += 1

    return result if result else None


def power_str_to_int(s: str):
    try:
        if s.endswith("M"):
            return int(float(s[:-1]) * 1_000_000)
        if s.endswith("K"):
            return int(float(s[:-1]) * 1_000)
        return int(s)
    except:
        return None


# ==========================
# ARENA FIGHT
# ==========================

class ArenaFight:
    def __init__(self, device_id):
        self.device_id = device_id
        self.white_tmpl, self.red_tmpl, self.letter_tmpl = load_templates()

    def capture(self):
        return adb_screencap(self.device_id, "__arena_screen.png")

    def read_row_power(self, screenshot, row_index):
        area = screenshot[POWER_Y1:POWER_Y2, POWER_X1:POWER_X2]
        if area.size == 0:
            return None

        s = read_power_number(
            area,
            start_x=0,
            white_tmpl=self.white_tmpl,
            red_tmpl=self.red_tmpl,
            letter_tmpl=self.letter_tmpl
        )
        if s is None:
            return None

        return power_str_to_int(s)

    def find_weakest_row(self, screenshot):
        weakest_row = None
        weakest_power = None

        for row in range(ARENA_ROWS):
            power = self.read_row_power(screenshot, row)
            if power is None:
                continue

            if weakest_power is None or power < weakest_power:
                weakest_power = power
                weakest_row = row

        return weakest_row

    def tap_row(self, row_index):
        x = 400
        y = FIRST_ROW_CENTER_Y + row_index * ROW_HEIGHT
        tap(self.device_id, x, y)

    def run_once(self):
        screenshot = self.capture()
        if screenshot is None:
            return

        row = self.find_weakest_row(screenshot)
        if row is None:
            return

        self.tap_row(row)


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m Ldplayer_bot.services.arena_fight <device_id>")
        sys.exit(1)

    DEVICE_ID = sys.argv[1]
    bot = ArenaFight(DEVICE_ID)

    while True:
        try:
            bot.run_once()
            time.sleep(3)
        except KeyboardInterrupt:
            break
