"""
Модуль графического интерфейса планера физических упражнений.
Создает настольное приложение с использованием tkinter.
"""

import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog

from models import Exercise
from storage import DataStorage
from utils import (
    validate_weight, validate_exercise_type,
    validate_comment, validate_date, validate_sets, validate_reps
)


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
            text="Дата (DD.MM.YYYY):"
        ).grid(
            row=4,
            column=0,
            sticky=tk.W,
            pady=5
        )
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
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
        try:
            # Валидация типа упражнения
            exercise_type_str = self.exercise_type_var.get()
            is_valid, cleaned_type, error_msg = validate_exercise_type(
                exercise_type_str
            )
            if not is_valid:
                messagebox.showerror(
                    "Ошибка",
                    f"Ошибка в типе упражнения: {error_msg}"
                )
                return

            # Валидация веса
            weight_str = self.weight_entry.get()
            is_valid, weight, error_msg = validate_weight(weight_str)
            if not is_valid:
                messagebox.showerror("Ошибка", f"Ошибка в весе: {error_msg}")
                return

            # Валидация подходов
            sets_str = self.sets_entry.get()
            is_valid, sets, error_msg = validate_sets(sets_str)
            if not is_valid:
                messagebox.showerror(
                    "Ошибка",
                    f"Ошибка в количестве подходов: {error_msg}"
                )
                return

            # Валидация повторений
            reps_str = self.reps_entry.get()
            is_valid, reps, error_msg = validate_reps(reps_str)
            if not is_valid:
                messagebox.showerror(
                    "Ошибка",
                    f"Ошибка в количестве повторений: {error_msg}"
                )
                return

            # Валидация даты
            date_str = self.date_entry.get()
            is_valid, date, error_msg = validate_date(date_str)
            if not is_valid:
                messagebox.showerror("Ошибка", f"Ошибка в дате: {error_msg}")
                return

            # Комментарий
            comment = validate_comment(self.comment_entry.get())

            # Создание упражнения
            exercise = Exercise(
                cleaned_type,
                weight,
                sets,
                reps,
                date,
                comment
            )

            # Сохранение
            self.storage.add_exercise(exercise)

            messagebox.showinfo("Успех", "Упражнение успешно добавлено!")

        except ValueError as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при добавлении упражнения: {e}"
            )
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Неожиданная ошибка: {e}"
            )