"""
Модуль для анализа данных о физических упражнениях.
Предоставляет функции для анализа тренировок с использованием pandas
и создания визуализаций с помощью matplotlib и seaborn.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from models import Exercise


class ExerciseAnalyzer:
    """
    Класс для анализа данных о физических упражнениях.
    """

    def __init__(self, exercises: List[Exercise]):
        """
        Инициализация анализатора.
        """
        self.exercises = exercises

    def to_dataframe(self) -> pd.DataFrame:
        """
        Преобразует список упражнений в DataFrame pandas.
        """
        if not self.exercises:
            return pd.DataFrame(columns=[
                'exercise_id', 'exercise_type', 'weight', 'sets',
                'reps', 'date', 'total_volume'
            ])

        data = []
        for ex in self.exercises:
            data.append({
                'exercise_id': ex.exercise_id,
                'exercise_type': ex.exercise_type,
                'weight': ex.weight,
                'sets': ex.sets,
                'reps': ex.reps,
                'date': ex.date,
                'comment': ex.comment,
                'total_volume': ex.get_total_volume()
            })

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_total_volume(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """
        Рассчитывает общий объем работы (кг) за период.
        """
        total = 0.0
        for exercise in self.exercises:
            if start_date and exercise.date < start_date:
                continue
            if end_date and exercise.date > end_date:
                continue

            total += exercise.get_total_volume()
        return total

    def get_volume_by_exercise_type(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """
        Возвращает объем работы по типам упражнений.
        """
        volume_by_type = {}

        for exercise in self.exercises:
            if start_date and exercise.date < start_date:
                continue
            if end_date and exercise.date > end_date:
                continue

            exercise_type = exercise.exercise_type
            volume_by_type[exercise_type] = volume_by_type.get(
                exercise_type, 0.0
            ) + exercise.get_total_volume()

        return volume_by_type

    def get_progress_by_exercise_type(
        self,
        exercise_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Tuple[datetime, float]]:
        """
        Возвращает прогресс по конкретному типу упражнения.
        """
        progress = []

        for exercise in self.exercises:
            if exercise.exercise_type != exercise_type:
                continue

            if start_date and exercise.date < start_date:
                continue
            if end_date and exercise.date > end_date:
                continue

            progress.append((
                exercise.date,
                exercise.weight
            ))

        # Сортируем по дате
        progress.sort(key=lambda x: x[0])
        return progress

    def get_max_weight_by_exercise_type(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """
        Возвращает максимальный вес по типам упражнений.
        """
        max_weights = {}

        for exercise in self.exercises:
            if start_date and exercise.date < start_date:
                continue
            if end_date and exercise.date > end_date:
                continue

            exercise_type = exercise.exercise_type
            if exercise_type not in max_weights:
                max_weights[exercise_type] = exercise.weight
            else:
                max_weights[exercise_type] = max(
                    max_weights[exercise_type], exercise.weight
                )

        return max_weights

    def plot_progress_over_time(
        self,
        exercise_type: str,
        output_file: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Строит график прогресса по весу для конкретного упражнения.
        """
        progress = self.get_progress_by_exercise_type(
            exercise_type, start_date, end_date
        )

        if not progress:
            print(f"Нет данных для упражнения '{exercise_type}'")
            return

        dates = [p[0] for p in progress]
        weights = [p[1] for p in progress]

        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 6))

        # График веса
        plt.plot(
            dates, weights, marker='o', linewidth=2,
            label='Используемый вес', color='blue'
        )
        plt.ylabel('Вес (кг)', fontsize=12)
        plt.xlabel('Дата', fontsize=12)
        plt.title(
            f'Прогресс по весу - {exercise_type}',
            fontsize=14, fontweight='bold'
        )
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def plot_volume_by_exercise_type_pie(
        self,
        output_file: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Строит круговую диаграмму объема работы по типам упражнений.
        """
        volume_by_type = self.get_volume_by_exercise_type(start_date, end_date)

        if not volume_by_type:
            print("Нет данных для построения диаграммы")
            return

        exercise_types = list(volume_by_type.keys())
        volumes = list(volume_by_type.values())

        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 8))
        plt.pie(
            volumes, labels=exercise_types,
            autopct='%1.1f%%', startangle=90
        )
        plt.title(
            'Распределение объема работы по типам упражнений',
            fontsize=14, fontweight='bold'
        )
        plt.axis('equal')

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def plot_max_weights_bar(
        self,
        output_file: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Строит столбчатую диаграмму максимальных весов по типам упражнений.
        """
        max_weights = self.get_max_weight_by_exercise_type(
            start_date, end_date
        )

        if not max_weights:
            print("Нет данных для построения графика")
            return

        exercise_types = list(max_weights.keys())
        weights = list(max_weights.values())

        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 6))
        colors = sns.color_palette("husl", len(exercise_types))
        plt.barh(exercise_types, weights, color=colors)
        plt.xlabel('Максимальный вес (кг)', fontsize=12)
        plt.ylabel('Тип упражнения', fontsize=12)
        plt.title(
            'Максимальные веса по типам упражнений',
            fontsize=14,
            fontweight='bold'
        )
        plt.gca().invert_yaxis()
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def plot_total_volume_over_time(
        self,
        output_file: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Строит график общего объема работы по времени.
        """
        df = self.to_dataframe()

        if df.empty:
            print("Нет данных для построения графика")
            return

        # Фильтрация по дате
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]

        if df.empty:
            print("Нет данных за выбранный период")
            return

        # Группировка по дате
        df['date_only'] = df['date'].dt.date
        daily_volume = df.groupby('date_only')['total_volume'].sum()

        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 6))
        plt.plot(
            daily_volume.index,
            daily_volume.values,
            marker='o',
            linewidth=2,
            color='purple'
        )
        plt.title(
            'Динамика общего объема работы',
            fontsize=14,
            fontweight='bold'
        )
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Объем работы (кг)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
