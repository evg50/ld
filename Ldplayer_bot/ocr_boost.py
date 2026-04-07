import cv2
import pytesseract
import re

# Укажи путь к Tesseract, если не добавлен в PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def clean(text):
    """
    Очищает результат OCR, извлекая число с запятой.
    """
    text = text.replace(".", ",")  # OCR часто путает запятую с точкой
    match = re.search(r"\d{1,3}(,\d{3})", text)
    return match.group(0) if match else text

def preprocess(img):
    """
    Преобразует изображение: оттенки серого, увеличение, сглаживание, бинаризация.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    blurred = cv2.medianBlur(resized, 3)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def test_ocr(img_path):
    """
    Тестирует OCR с разными режимами PSM и OEM.
    """
    img = cv2.imread(img_path)
    if img is None:
        print("❌ Изображение не найдено:", img_path)
        return

    processed = preprocess(img)

    print("📊 OCR тестирование:")
    for psm in [6, 7, 8, 11]:
        for oem in [1, 3]:
            config = f"--psm {psm} --oem {oem}"
            text = pytesseract.image_to_string(processed, lang="eng", config=config)
            result = clean(text.strip())
            print(f"🔧 PSM={psm}, OEM={oem} → {result}")

if __name__ == "__main__":
    test_ocr("debug_power.png")
