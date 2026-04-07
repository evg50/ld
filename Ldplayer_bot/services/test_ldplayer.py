from ldplayer_manager import start_emulator_and_game

print("=== ТЕСТ ЗАПУСКА ЭМУЛЯТОРА ===")
DEVICE_ID = start_emulator_and_game(index=3)
print("DEVICE_ID:", DEVICE_ID)

