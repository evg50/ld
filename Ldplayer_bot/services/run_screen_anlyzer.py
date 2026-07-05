#!/usr/bin/env python3
"""
run_test_recognize.py

Запуск тестовой утилиты `test_recognize_on_folder` для модуля, содержащего
реализацию recognize_screen и тестовой функции.

Ожидается, что реализация находится в файле `screen_recognizer.py` в той же папке
и экспортирует функцию `test_recognize_on_folder(device_id_for_path, test_folder)`.

Пример запуска:
    python run_test_recognize.py
    python run_test_recognize.py --test-folder "C:\Ldplayer_bot\Ldplayer_bot\screenshots\test" --device-id test_device
"""

import os
import argparse
import logging
from pprint import pprint

# Импортируем тестовую функцию из модуля с реализацией.
# Если ваш файл называется иначе, измените импорт ниже.
try:

    from Ldplayer_bot.services.screen_analyzer  import test_recognize_on_folder

    
except Exception as e:
    raise ImportError(
        "Не удалось импортировать test_recognize_on_folder из screen_recognizer.py. "
        "Убедитесь, что файл с реализацией называется screen_recognizer.py и находится в той же папке."
    ) from e

# Настройка логирования (краткие логи)
logger = logging.getLogger("run_test_recognize")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Run recognize_screen tests on a folder of screenshots.")
    parser.add_argument(
        "--test-folder",
        "-t",
        default=r"C:\Ldplayer_bot\Ldplayer_bot\screenshots\test",
        help="Путь к папке с тестовыми скриншотами (по умолчанию C:\\Ldplayer_bot\\Ldplayer_bot\\screenshots\\test).",
    )
    parser.add_argument(
        "--device-id",
        "-d",
        default="test_device",
        help="DEVICE_ID, который будет передан в test_recognize_on_folder (по умолчанию 'test_device').",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Опционально: путь к файлу для сохранения результатов в формате plain text (каждая строка: filename -> result).",
    )

    args = parser.parse_args()

    test_folder = os.path.abspath(args.test_folder)
    device_id = args.device_id
    output_file = args.output

    logger.info(f"Test folder: {test_folder}")
    logger.info(f"Device ID: {device_id}")

    if not os.path.isdir(test_folder):
        logger.error(f"Тестовая папка не найдена: {test_folder}")
        return

    logger.info("Запуск тестов...")
    results = test_recognize_on_folder(device_id, test_folder)

    logger.info("Результаты тестов:")
    pprint(results)

    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for fname, res in results.items():
                    f.write(f"{fname} -> {res}\n")
            logger.info(f"Результаты сохранены в {output_file}")
        except Exception as e:
            logger.error(f"Не удалось сохранить результаты в {output_file}: {e}")


if __name__ == "__main__":
    main()
