import os
import cv2

DEVICE = "127.0.0.1:5557"
SCREENSHOT_PATH = "screen.png"

# Сделать скриншот с LDPlayer
os.system(f'adb -s {DEVICE} exec-out screencap -p > {SCREENSHOT_PATH}')

# Открыть изображение
image = cv2.imread(SCREENSHOT_PATH)

# Показать окно с изображением
cv2.imshow("LDPlayer Screenshot", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
