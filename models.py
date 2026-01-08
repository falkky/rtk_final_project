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

        exercise_type_clean = exercise_type.strip()
        if not exercise_type_clean:
            raise ValueError("Тип упражнения не может быть пустым")
        self.exercise_type = exercise_type_clean

        weight_val = float(weight)
        if weight_val < 0:
            raise ValueError("Вес не может быть отрицательным")
        self.weight = weight_val

        sets_val = int(sets)
        if sets_val <= 0:
            raise ValueError("Количество подходов должно быть положительным")
        self.sets = sets_val

        reps_val = int(reps)
        if reps_val <= 0:
            raise ValueError("Количество повторений должно быть положительным")
        self.reps = reps_val

        # date can be a datetime or a string; keep as provided
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
