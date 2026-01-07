"""
Модуль графического интерфейса планера физических упражнений.
Создает настольное приложение с использованием tkinter.
"""

import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog

from analysis import ExerciseAnalyzer
from models import Exercise
from storage import DataStorage


class ExercisePlannerGUI:
    """
    Класс для графического интерфейса планера упражнений.
    """

    def __init__(self, root: tk.Tk, storage: DataStorage):
        """
        Инициализация GUI.
        """
        self.root = root
        self.storage = storage
        self.analyzer = ExerciseAnalyzer(self.storage.get_all_exercises())

        self.root.title("Планер физических упражнений")
        self.root.geometry("1200x750")
