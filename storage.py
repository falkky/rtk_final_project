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
        try:
            with open(self.csv_file, 'w', encoding='utf-8', newline='') as file:
                if not self.exercises:
                    # Создаем заголовки даже если данных нет
                    writer = csv.DictWriter(file, fieldnames=[
                        'exercise_id', 'exercise_type', 'weight',
                        'sets', 'reps', 'date', 'comment'
                    ])
                    writer.writeheader()
                    return

                writer = csv.DictWriter(file, fieldnames=[
                    'exercise_id', 'exercise_type', 'weight',
                    'sets', 'reps', 'date', 'comment'
                ])

                writer.writeheader()

                for exercise in self.exercises:
                    writer.writerow(exercise.to_dict())
        except IOError as e:
            raise IOError(f"Ошибка при записи файла {self.csv_file}: {e}")

    def add_exercise(self, exercise: Exercise) -> Exercise:
        """
        Добавляет новое упражнение в хранилище.
        """
        if exercise.exercise_id == 0:
            exercise.exercise_id = self.next_id
            self.next_id += 1

        self.exercises.append(exercise)
        self.save_data()
        return exercise