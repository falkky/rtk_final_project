"""
Главный файл планера физических упражнений.
Точка входа в приложение. Инициализирует хранилище данных и запускает GUI.
"""

import tkinter as tk
import sys

from gui import ExercisePlannerGUI
from storage import DataStorage


def main():
    """
    Главная функция приложения.
    Создает хранилище данных и запускает графический интерфейс.
    """
    try:
        # Инициализация хранилища данных
        storage = DataStorage("data/exercises_data.csv")

        # Создание главного окна
        root = tk.Tk()

        # Создание и запуск GUI
        ExercisePlannerGUI(root, storage)

        # Запуск главного цикла событий
        root.mainloop()

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
