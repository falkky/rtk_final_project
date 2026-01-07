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
