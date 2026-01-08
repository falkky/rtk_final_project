"""
Модуль для сохранения и загрузки данных о физических упражнениях.
Обеспечивает работу с CSV файлами для хранения упражнений.
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Optional

from models import Exercise


class DataStorage:
    """
    Класс для работы с хранилищем данных (CSV файл).
    """

    def __init__(self, csv_file: str = "data/exercises_data.csv"):
        """
        Инициализация хранилища данных.
        """
        self.csv_file = csv_file
        self.exercises: List[Exercise] = []
        self.next_id = 1

        # Создаем директорию
        directory_path = os.path.dirname(csv_file)
        os.makedirs(directory_path, exist_ok=True)

        # Загружаем данные при инициализации
        # self.load_data()

    def load_data(self) -> None:
        """
        Загружает данные из CSV файла.
        """

    def save_data(self) -> None:
        """
        Сохраняет данные в CSV файл.
        """