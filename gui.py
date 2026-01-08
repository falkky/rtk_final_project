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
        self.analyzer = ExerciseAnalyzer(self.storage.get_all_exercises())

        self.root.title("Планер физических упражнений")
        self.root.geometry("1200x750")

        self.create_widgets()
        self.refresh_exercises_list()
        self.update_statistics()

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
        self.update_exercise_type_list()

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

        # Фильтры
        filter_frame = ttk.Frame(list_frame)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(filter_frame, text="Тип:").grid(row=0, column=0, padx=5)
        self.filter_type = tk.StringVar(value="all")
        self.type_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type,
            width=15,
            state="readonly"
        )
        self.type_combobox.grid(row=0, column=1, padx=5)
        self.update_type_filter()
        ttk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.refresh_exercises_list
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            filter_frame,
            text="Сбросить",
            command=self.reset_filter
        ).grid(row=0, column=3, padx=5)

        # Список упражнений
        tree_frame = ttk.Frame(list_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = (
            "ID",
            "Тип",
            "Вес",
            "Подходы",
            "Повторения",
            "Дата",
            "Комментарий"
        )
        self.exercises_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.exercises_tree.heading(col, text=col)
            if col == "ID":
                self.exercises_tree.column(col, width=50)
            elif col == "Комментарий":
                self.exercises_tree.column(col, width=150)
            else:
                self.exercises_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self.exercises_tree.yview
        )
        self.exercises_tree.configure(yscrollcommand=scrollbar.set)

        self.exercises_tree.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Кнопки управления упражнениями
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.grid(row=2, column=0, pady=10)

        ttk.Button(
            buttons_frame,
            text="Удалить выбранное",
            command=self.delete_selected_exercise
        ).grid(row=0, column=0, padx=5)

        # Нижняя панель - анализ и графики
        analysis_frame = ttk.LabelFrame(
            main_frame,
            text="Анализ и графики",
            padding="10"
        )
        analysis_frame.grid(
            row=2, column=0, columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(10, 0)
        )

        ttk.Label(
            analysis_frame,
            text="Выберите упражнение для анализа:"
        ).grid(row=0, column=0, padx=5)

        self.analysis_exercise_type = tk.StringVar()

        self.analysis_type_combobox = ttk.Combobox(
            analysis_frame,
            textvariable=self.analysis_exercise_type,
            width=20,
            state="readonly"
        )
        self.analysis_type_combobox.grid(row=0, column=1, padx=5)
        self.update_analysis_types()

        ttk.Button(
            analysis_frame,
            text="Прогресс по весу",
            command=self.plot_progress
        ).grid(row=0, column=2, padx=5)
        ttk.Button(
            analysis_frame,
            text="Круговая диаграмма объема",
            command=self.plot_volume_pie
        ).grid(row=0, column=3, padx=5)
        ttk.Button(
            analysis_frame,
            text="Максимальные веса",
            command=self.plot_max_weights
        ).grid(row=0, column=4, padx=5)
        ttk.Button(
            analysis_frame,
            text="Динамика объема",
            command=self.plot_volume_over_time
        ).grid(row=0, column=5, padx=5)

        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(
            label="Экспорт в CSV...",
            command=self.export_to_csv
        )
        file_menu.add_command(
            label="Экспорт в JSON...",
            command=self.export_to_json
        )

        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

    def get_exercise_types(self) -> list:
        """Возвращает список всех типов упражнений."""
        exercises = self.storage.get_all_exercises()
        return sorted(set([ex.exercise_type for ex in exercises]))

    def update_exercise_type_list(self) -> None:
        """Обновляет список типов упражнений для поля ввода."""
        exercise_types = self.get_exercise_types()
        self.exercise_type_entry['values'] = exercise_types

    def update_type_filter(self) -> None:
        """Обновляет список типов упражнений для фильтра."""
        exercise_types = self.get_exercise_types()
        self.type_combobox['values'] = ["all"] + exercise_types

    def update_analysis_types(self) -> None:
        """Обновляет список типов упражнений для анализа."""
        exercise_types = self.get_exercise_types()
        self.analysis_type_combobox['values'] = exercise_types
        if exercise_types:
            self.analysis_exercise_type.set(exercise_types[0])

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
            self.analyzer = ExerciseAnalyzer(
                self.storage.get_all_exercises()
            )

            # Очистка полей после добавления
            self.exercise_type_var.set("")
            self.weight_entry.delete(0, tk.END)
            self.sets_entry.delete(0, tk.END)
            self.reps_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
            self.comment_entry.delete(0, tk.END)

            # Обновление интерфейса
            self.update_exercise_type_list()
            self.update_type_filter()
            self.update_analysis_types()
            self.refresh_exercises_list()
            self.update_statistics()

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

    def delete_selected_exercise(self) -> None:
        """Удаляет выбранное упражнение."""
        selected = self.exercises_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите упражнение для удаления"
            )
            return

        try:
            item = self.exercises_tree.item(selected[0])
            exercise_id = int(item['values'][0])

            if messagebox.askyesno(
                "Подтверждение",
                "Вы уверены, что хотите удалить это упражнение?"
            ):
                self.storage.remove_exercise(exercise_id)
                self.analyzer = ExerciseAnalyzer(
                    self.storage.get_all_exercises()
                )
                self.update_exercise_type_list()
                self.update_type_filter()
                self.update_analysis_types()
                self.refresh_exercises_list()
                self.update_statistics()
                messagebox.showinfo("Успех", "Упражнение удалено")
        except (ValueError, IndexError) as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при удалении упражнения: {e}"
            )

    def refresh_exercises_list(self) -> None:
        """Обновляет список упражнений с учетом фильтров."""

        # Очистка списка
        for item in self.exercises_tree.get_children():
            self.exercises_tree.delete(item)

        # Получение упражнений с учетом фильтра
        filter_type = self.filter_type.get()
        exercises = self.storage.get_all_exercises()

        if filter_type != "all":
            exercises = [
                ex for ex in exercises
                if ex.exercise_type == filter_type
            ]

        # Сортировка по дате (новые сначала)
        exercises.sort(
            key=lambda x: x.date,
            reverse=True
        )

        # Заполнение списка
        for exercise in exercises:
            self.exercises_tree.insert("", tk.END, values=(
                exercise.exercise_id,
                exercise.exercise_type,
                exercise.weight,
                exercise.sets,
                exercise.reps,
                exercise.date.strftime("%Y-%m-%d"),
                (
                    exercise.comment[:30] + "..."
                    if len(exercise.comment) > 30
                    else exercise.comment
                )
            ))

    def reset_filter(self) -> None:
        """Сбрасывает фильтры."""
        self.filter_type.set("all")
        self.refresh_exercises_list()

    def update_statistics(self) -> None:
        """Обновляет статистику в верхней панели."""
        try:
            total_volume = self.analyzer.get_total_volume()
            exercises_list = self.storage.get_all_exercises()
            total_exercises = len(exercises_list)
            exercise_types = len(
                {ex.exercise_type for ex in exercises_list}
            )

            self.total_volume_label.config(
                text=f"Общий объем: {total_volume}"
            )
            self.total_exercises_label.config(
                text=f"Всего упражнений: {total_exercises}"
            )
            self.exercise_types_label.config(
                text=f"Типов упражнений: {exercise_types}"
            )
        except Exception as e:
            print(
                f"Ошибка при обновлении статистики: {e}"
            )

    def plot_progress(self) -> None:
        """Строит график прогресса по весу."""
        try:
            exercise_type = self.analysis_exercise_type.get()
            if not exercise_type:
                messagebox.showwarning(
                    "Предупреждение",
                    "Выберите тип упражнения для анализа"
                )
                return
            self.analyzer.plot_progress_over_time(exercise_type)
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при построении графика: {e}"
            )

    def plot_volume_pie(self) -> None:
        """Строит круговую диаграмму объема работы."""
        try:
            self.analyzer.plot_volume_by_exercise_type_pie()
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при построении диаграммы: {e}"
            )

    def plot_max_weights(self) -> None:
        """Строит график максимальных весов."""
        try:
            self.analyzer.plot_max_weights_bar()
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Ошибка при построении графика: {e}"
            )

    def plot_volume_over_time(self) -> None:
        """Строит график динамики объема работы."""
        try:
            self.analyzer.plot_total_volume_over_time()
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Ошибка при построении графика: {e}"
            )

    def export_to_json(self) -> None:
        """Экспортирует данные в JSON."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.storage.export_to_JSON(filename)
                messagebox.showinfo(
                    "Успех",
                    f"Данные экспортирована в {filename}"
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {e}")

    def export_to_csv(self) -> None:
        """Экспортирует данные в CSV."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                self.storage.export_to_csv(filename)
                messagebox.showinfo(
                    "Успех", f"Данные экспортированы в {filename}"
                )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {e}")
