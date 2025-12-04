import cv2
import pytesseract

def check_text_in_region(img, region, expected_text, lang="eng", debug=False):
    """
    Проверяет, содержится ли expected_text в указанной области изображения.
    region: (x1, y1, x2, y2)
    expected_text: строка, которую ожидаем найти
    lang: язык OCR ("eng", "rus" и т.д.)
    debug: если True — сохраняет вырезанную область
    """
    x1, y1, x2, y2 = region
    cropped = img[y1:y2, x1:x2]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    text = pytesseract.image_to_string(resized, lang=lang, config="--psm 7").strip().lower()

    if debug:
        cv2.imwrite("debug/ocr_region.png", resized)
        print(f"🔍 OCR: {text}")

    return expected_text.lower() in text