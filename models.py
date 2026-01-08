"""
Модуль для моделей данных планера физических упражнений.
Содержит класс для представления упражнений.
"""

from datetime import datetime


class Exercise:
    """
    Класс для физического упражнения.
    """

    def __init__(
        self,
        exercise_type: str,
        weight: float,
        sets: int,
        reps: int,
        date: datetime,
        comment: str = "",
        exercise_id: int = 0
    ):
        """
        Инициализация упражнения.
        """

        self.exercise_type = exercise_type.strip()
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.date = date
        self.comment = comment
        self.exercise_id = exercise_id
