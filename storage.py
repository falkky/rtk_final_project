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
        self.load_data()

    def load_data(self) -> None:
        """
        Загружает данные из CSV файла.
        """
        self.exercises = []
        self.next_id = 1

        if not os.path.exists(self.csv_file):
            return

        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        exercise = Exercise.from_dict({
                            'exercise_id': int(row.get('exercise_id', 0)),
                            'exercise_type': row['exercise_type'],
                            'weight': float(row['weight']),
                            'sets': int(row['sets']),
                            'reps': int(row['reps']),
                            'date': row['date'],
                            'comment': row.get('comment', '')
                        })
                        self.exercises.append(exercise)

                        # Обновляем next_id
                        if exercise.exercise_id > 0 and exercise.exercise_id >= self.next_id:
                            self.next_id = exercise.exercise_id + 1
                    except (ValueError, KeyError) as e:
                        # Пропускаем некорректные записи
                        print(f"Предупреждение: пропущена некорректная запись: {e}")
                        continue
        except IOError as e:
            raise IOError(f"Ошибка при чтении файла {self.csv_file}: {e}")

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

    def remove_exercise(self, exercise_id: int) -> bool:
        """
        Удаляет упражнение по ID.
        """
        initial_length = len(self.exercises)
        self.exercises = [
            ex for ex in self.exercises if ex.exercise_id != exercise_id
        ]

        if len(self.exercises) < initial_length:
            self.save_data()
            return True
        return False

    def get_all_exercises(self) -> List[Exercise]:
        """
        Возвращает список всех упражнений.
        """
        return self.exercises.copy()

    def export_to_csv(self, output_file: str) -> None:
        """
        Экспортирует данные в указанный CSV файл.
        """
        try:
            os.makedirs(
                os.path.dirname(output_file) if os.path.dirname(output_file) else '.',
                exist_ok=True
            )

            with open(output_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'exercise_id', 'exercise_type', 'weight',
                    'sets', 'reps', 'date', 'comment'
                ])
                writer.writeheader()

                for exercise in self.exercises:
                    writer.writerow(exercise.to_dict())
        except IOError as e:
            raise IOError(f"Ошибка при экспорте в {output_file}: {e}")

    def export_to_JSON(self, output_file: str) -> None:
        """
        Экспортирует данные в указанный JSON файл.
        """
        try:
            os.makedirs(
                os.path.dirname(output_file) if os.path.dirname(output_file) else '.',
                exist_ok=True
            )
            exercises_data = [exercise.to_dict() for exercise in self.exercises]
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(exercises_data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            raise IOError(f"Ошибка при экспорте в {output_file}: {e}")
