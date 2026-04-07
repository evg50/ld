import cv2
import pytesseract
import re
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_number(img, region):
    x1, y1, x2, y2 = region
    cropped = img[y1:y2, x1:x2]

    os.makedirs("debug", exist_ok=True)
    cv2.imwrite("debug/debug_power_raw.png", cropped)

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

    cv2.imwrite("debug/debug_power_filtered.png", thresh)

    config = "--psm 7 -c tessedit_char_whitelist=0123456789,"
    raw = pytesseract.image_to_string(thresh, lang="eng", config=config)
    cleaned = raw.strip().replace(" ", "").replace(".", ",")
    
    # Удалим все символы, кроме цифр и запятых
    cleaned = re.sub(r"[^\d,]", "", cleaned)

    # Если число вида 1230,509 — заменим первую запятую на точку, потом уберём вторую
    if cleaned.count(",") == 1 and len(cleaned.split(",")[0]) > 3:
        cleaned = cleaned.replace(",", "", 1)

    # Удалим все запятые и вернём как строку
    return cleaned

def parse_number(text):
    return int(text.replace(",", "")) if text else 0

def read_text(img, region):
    """
    Распознаёт обычный текст (например, ник или сервер), убирает лишние символы.
    """
    x1, y1, x2, y2 = region
    cropped = img[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    text = pytesseract.image_to_string(resized, lang="eng", config="--psm 7")
    cleaned = re.sub(r"[^a-zA-Z0-9#\- ]", "", text.strip())
    return cleaned

def get_loot_info():
    img = cv2.imread("screenshots/screen.png")
    if img is None:
        print("❌ Скриншот не найден")
        return {}

    # Координаты — подстрой под свой экран
    POWER_REGION = (355 , 1430, 545, 1465)
    NAME_REGION = (400, 1353, 500, 1375)
    SERVER_REGION = (325, 1350, 400, 1375)

    power_raw = read_number(img, POWER_REGION)
    power = parse_number(power_raw)
    name = read_text(img, NAME_REGION)
    server = read_text(img, SERVER_REGION)

    return {
        "power": power,
        "name": name,
        "server": server
    }

if __name__ == "__main__":
    info = get_loot_info()
    print("📦 Результат OCR:")
    print(info)

