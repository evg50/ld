import sys
import time

from Ldplayer_bot.services.saga_handler import run_saga
from Ldplayer_bot.services.saga_init import is_saga_screen


def main():
    if len(sys.argv) < 3:
        print("Usage: python saga_run.py <DEVICE_ID> <solo|raid>")
        sys.exit(1)

    DEVICE_ID = sys.argv[1]
    MODE = sys.argv[2].lower()

    if MODE not in ("solo", "raid"):
        print("Mode must be: solo or raid")
        sys.exit(1)

    solo = MODE == "solo"
    raid = MODE == "raid"

    print(f"Device: {DEVICE_ID}")
    print(f"Mode: {MODE.upper()}")
    print("Starting saga loop...")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n=== Saga cycle {cycle} ===")

        # Если экран саги появился — останавливаемся
        if is_saga_screen(DEVICE_ID):
            print("Saga screen detected -> stopping")
            break
        
        # Иначе запускаем сагу
        result = run_saga(DEVICE_ID, solo=solo, raid=raid)

        if not result:
            print("Saga failed -> retrying in 3 sec")
            time.sleep(3)
            continue

        print("Saga started successfully")
        time.sleep(2)

    print("\nSaga loop finished.")


if __name__ == "__main__":
    main()
