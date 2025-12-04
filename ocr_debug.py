import cv2
import pytesseract
import re
import os

# Укажи путь к Tesseract, если не добавлен в PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Координаты области силы (подстрой под свой экран)
POWER_REGION = (355, 1430, 545, 1465)

def extract_region(img, region):
    x1, y1, x2, y2 = region
    return img[y1:y2, x1:x2]

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)
    return thresh

def tesseract_ocr(img):
    config = "--psm 7 -c tessedit_char_whitelist=0123456789,"
    raw = pytesseract.image_to_string(img, lang="eng", config=config)
    cleaned = raw.strip().replace(" ", "").replace(".", ",")

    # Если шаблон не сработал — вернём всю строку
    match = re.search(r"\d{1,3}(,\d{3}){1,2}", cleaned)
    final = match.group(0) if match else cleaned
    return raw.strip(), final

def save_debug_images(original, filtered):
    os.makedirs("debug", exist_ok=True)
    cv2.imwrite("debug/debug_power_raw.png", original)
    cv2.imwrite("debug/debug_power_filtered.png", filtered)

def main():
    img = cv2.imread("screenshots/screen.png")
    if img is None:
        print("❌ Скриншот не найден")
        return

    region = extract_region(img, POWER_REGION)
    filtered = preprocess(region)
    save_debug_images(region, filtered)

    print("🔍 Tesseract OCR:")
    raw, final = tesseract_ocr(filtered)
    print("🧪 RAW:", raw)
    print("✅ CLEANED:", final)

if __name__ == "__main__":
    main()

