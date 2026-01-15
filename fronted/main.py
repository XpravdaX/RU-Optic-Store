import customtkinter as ctk
import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import OpticStoreAPI
import tkinter.messagebox as messagebox

# Проверяем, есть ли модуль main_window
try:
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Текущая директория:", os.getcwd())
    print("Файлы в директории:", os.listdir('.'))
    if 'ui' in os.listdir('.'):
        print("Файлы в ui:", os.listdir('ui'))
    sys.exit(1)


def main():
    # Проверить подключение к API
    api = OpticStoreAPI()

    if not api.check_connection():
        result = messagebox.askretrycancel(
            "Ошибка подключения",
            "Не удалось подключиться к серверу API.\n"
            "Убедитесь, что сервер запущен на http://127.0.0.1:8000\n\n"
            "Хотите попробовать снова?"
        )
        if result:
            main()
        return

    # Запустить приложение
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()