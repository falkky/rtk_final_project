"""
Модуль графического интерфейса планера физических упражнений.
Создает настольное приложение с использованием tkinter.
"""

import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog

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
        self.root.title("Планер физических упражнений")
        self.root.geometry("1200x750")

        self.create_widgets()

    def create_widgets(self) -> None:
        """Создает все виджеты интерфейса."""
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Статистика
        stats_frame = ttk.LabelFrame(
            main_frame, text="Статистика", padding="10"
        )
        stats_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 10)
        )

        self.total_volume_label = ttk.Label(
            stats_frame,
            text="Общий объем: 0 кг",
            font=("Arial", 12, "bold")
        )
        self.total_volume_label.grid(row=0, column=0, padx=10)
        self.total_exercises_label = ttk.Label(
            stats_frame,
            text="Всего упражнений: 0",
            font=("Arial", 10)
        )
        self.total_exercises_label.grid(row=0, column=1, padx=10)

        self.exercise_types_label = ttk.Label(
            stats_frame,
            text="Типов упражнений: 0",
            font=("Arial", 10)
        )
        self.exercise_types_label.grid(row=0, column=2, padx=10)

        # Левая панель - форма добавления упражнения
        form_frame = ttk.LabelFrame(
            main_frame,
            text="Добавить упражнение",
            padding="10"
        )
        form_frame.grid(
            row=1,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=(0, 10)
        )

        # Тип упражнения
        ttk.Label(
            form_frame,
            text="Тип упражнения:"
        ).grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.exercise_type_var = tk.StringVar()
        self.exercise_type_entry = ttk.Combobox(
            form_frame, textvariable=self.exercise_type_var, width=18
        )
        self.exercise_type_entry.grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5
        )

        # Вес
        ttk.Label(
            form_frame,
            text="Вес (кг):"
        ).grid(
            row=1,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.weight_entry = ttk.Entry(form_frame, width=20)
        self.weight_entry.grid(
            row=1,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5
        )

        # Количество подходов
        ttk.Label(
            form_frame,
            text="Подходы:"
        ).grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.sets_entry = ttk.Entry(form_frame, width=20)
        self.sets_entry.grid(
            row=2,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5
        )

        # Количество повторений
        ttk.Label(
            form_frame,
            text="Повторения:"
        ).grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.reps_entry = ttk.Entry(form_frame, width=20)
        self.reps_entry.grid(
            row=3,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5
        )

        # Дата
        ttk.Label(
            form_frame,
            text="Дата (YYYY-MM-DD):"
        ).grid(
            row=4,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(
            row=4,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5
        )

        # Комментарий
        ttk.Label(
            form_frame,
            text="Комментарий:"
        ).grid(
            row=5,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.comment_entry = ttk.Entry(form_frame, width=20)
        self.comment_entry.grid(
            row=5,
            column=1,
            sticky=(tk.W, tk.E),
            pady=5
        )
        add_button = ttk.Button(
            form_frame,
            text="Добавить упражнение",
            command=self.add_exercise
        )
        add_button.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=10
        )

        # Правая панель - список упражнений и фильтры
        list_frame = ttk.LabelFrame(
            main_frame,
            text="Упражнения",
            padding="10"
        )
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)

    def add_exercise(self) -> None:
        """Добавляет новое упражнение."""
        pass