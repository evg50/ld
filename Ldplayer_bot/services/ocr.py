



import cv2
import numpy as np
import pytesseract



def load_templates():
    base = r"C:\Ldplayer_bot\Ldplayer_bot\templates\numbers"

    white_tmpl = {}
    red_tmpl = {}
    letter_tmpl = {}

    for fname in os.listdir(base):
        if not fname.endswith(".png"):
            continue

        path = os.path.join(base, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        name = fname.replace(".png", "")

        # белые цифры: 0.png, 1.png, 2.png ...
        if name.isdigit():
            white_tmpl[name] = img
            continue

        # красные цифры: 0r.png, 1r.png ...
        if name.endswith("r") and name[:-1].isdigit():
            red_tmpl[name[:-1]] = img
            continue

        # буквы и точка: K.png, M.png, dot.png
        letter_tmpl[name] = img

    return white_tmpl, red_tmpl, letter_tmpl

def match_symbol(slice_img, templates, threshold=0.85):
    best_char = None
    best_score = 0
    best_width = 0

    for char, tmpl in templates.items():
        th, tw = tmpl.shape[:2]

        if slice_img.shape[1] < tw:
            continue

        region = slice_img[:, :tw]
        res = cv2.matchTemplate(region, tmpl, cv2.TM_CCOEFF_NORMED)
        score = res[0][0]

        if score > best_score and score >= threshold:
            best_score = score
            best_char = char
            best_width = tw

    return best_char, best_width

def read_power_number(area, debug_save_path=None):
    
    
    # 1. Увеличиваем изображение
    area = cv2.resize(area, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    b, g, r = cv2.split(area)

    # 2. Красный текст
    mask_red = (
        (r > 150) &
        (r.astype(int) - g.astype(int) > 40) &
        (r.astype(int) - b.astype(int) > 40)
    )
    mask_red = mask_red.astype(np.uint8) * 255

    # 3. Обводка белого текста
    mask_outline = (
        (r < 150) &
        (g < 150) &
        (b < 150)
    )
    mask_outline = mask_outline.astype(np.uint8) * 255

    kernel = np.ones((3, 3), np.uint8)
    mask_outline = cv2.dilate(mask_outline, kernel, iterations=2)

    # 4. Объединяем маски
    mask = cv2.bitwise_or(mask_red, mask_outline)

    filtered = cv2.bitwise_and(area, area, mask=mask)

    # 5. Монохром
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # >>> СОХРАНЕНИЕ ИТОГОВОЙ КАРТИНКИ <<<
    if debug_save_path:
        cv2.imwrite(debug_save_path, thresh)
    # >>> КОНЕЦ ДОБАВЛЕНИЯ <<<

    # 6. OCR
    config = "--psm 7 -c tessedit_char_whitelist=0123456789.M"
    text = pytesseract.image_to_string(thresh, config=config)

    if not text:
        return None

    text = text.strip().replace(" ", "").replace(",", ".").upper()
    text = text.replace("O", "0").replace("I", "1")

    try:
        if "M" in text:
            text = text.replace("M", "")
            value = float(text) * 1_000_000
        else:
            value = float(text)
    except:
        return None

    return int(value)

