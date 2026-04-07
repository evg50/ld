import cv2

img = cv2.imread("screen.png")
if img is None:
    print("❌ Файл повреждён или не является изображением.")
else:
    print("✅ Файл загружен успешно!")
   
    cv2.imshow("Скриншот LDPlayer", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
