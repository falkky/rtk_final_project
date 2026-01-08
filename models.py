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

    def get_total_volume(self) -> float:
        """
        Рассчитывает общий объем работы (вес × подходы × повторения).
        """
        return self.weight * self.sets * self.reps

    def to_dict(self) -> dict:
        """
        Преобразует упражнение в словарь для сериализации.
        """
        return {
            'exercise_id': self.exercise_id,
            'exercise_type': self.exercise_type,
            'weight': self.weight,
            'sets': self.sets,
            'reps': self.reps,
            'date': self.date.isoformat(),
            'comment': self.comment
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Exercise':
        """
        Создает упражнение из словаря.
        """
        date = datetime.fromisoformat(data['date'])

        return cls(
            exercise_type=data['exercise_type'],
            weight=float(data['weight']),
            sets=int(data['sets']),
            reps=int(data['reps']),
            date=date,
            comment=data.get('comment', ''),
            exercise_id=data.get('exercise_id')
        )
