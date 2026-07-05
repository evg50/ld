функція определения єкрана . текстовое задание



Предпосылки

from Ldplayer\_bot.adb import take\_screenshot, tap, BASE\_DIR
find\_match в єтом файле 

Разрешение экрана: 540 × 960.

from Ldplayer\_bot.vision.vision import check\_area\_xyxy

Используемые функции (существующие):



**take\_screenshot(DEVICE\_ID) — делает скриншот и сохраняет в BASE\_DIR/screenshots/<DEVICE\_ID>/screen.png.**



**find\_match(screenshot\_path, template\_path, area=None, threshold=0.7) — возвращает (cx, cy, score) или None.**



**check\_area\_xyxy(screenshot\_path, area\_xyxy, template\_path) — возвращает True/False.**



**tap(DEVICE\_ID, x, y) — тап по координатам.**



**Пути к шаблонам формировать через BASE\_DIR, например: os.path.join(BASE\_DIR, "templates", "buttons", "event\_btn.png").**



**Поведение при ошибке: при отсутствии ожидаемого шаблона на любом шаге — немедленно прервать выполнение и вернуть/залогировать ошибку с указанием шага и имени шаблона.**

**SCREENSHOT\_PATH = os.path.join(BASE\_DIR, "screenshots", DEVICE\_ID, "screen.png")**

**функция вида 
def recognize\_screen(DEVICE\_ID ):

проверяет зону (430, 865, 540, 960),

и ищет там SCREENSHOT\_PATH,**

&#x20;       **os.path.join(BASE\_DIR, "templates/buttons/world\_btn.png"),
если тру  возрващает "screen\_HQ"**

\*\*проверяет зону (430, 865, 540, 960),

и ищет там SCREENSHOT\_PATH,\*\*

&#x20;       **os.path.join(BASE\_DIR, "templates/buttons/hq\_btn.png"),
если тру  возрващает "screen\_world"
если 
find\_match(**

&#x20;       **SCREENSHOT\_PATH,**

&#x20;       **os.path.join(BASE\_DIR, "templates/buttons/march.png"),**

&#x20;       **area=(150, 600, 350, 720),**

&#x20;       **threshold=0.85
вернуть screen\_world\_march**



**если find\_match(**

&#x20;       **SCREENSHOT\_PATH,**

&#x20;       **os.path.join (BASE\_DIR, "templates/buttons", "others' Trucks\_btn.png")**

&#x20;       **area = (90, 890, 300, 950)**        **threshold=0.6
	return screen\_truck\_plunder

screenshot = refresh\_screenshot(device\_id)**

&#x20;   **area = (11, 13, 190, 65)**

&#x20;   **template = os.path.join(BASE\_DIR, "templates", "saga\_screen.png")**

&#x20;   **ok = check\_area\_xyxy(screenshot, template, area)**



&#x20;   **print(f"\[CHECK] saga\_screen -> {ok}")**

&#x20;   

&#x20;   **return screen\_saga**




