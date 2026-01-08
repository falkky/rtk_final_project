"""
Модуль с вспомогательными функциями для планера физических упражнений.
Содержит функции для валидации данных, форматирования и работы с
регулярными выражениями.
"""

import re
from datetime import datetime
from typing import Optional, Tuple


def validate_weight(weight_str: str) -> Tuple[
        bool,
        Optional[float],
        Optional[str]
        ]:
    """
    Валидация веса с использованием регулярных выражений.
    """
    weight = weight_str.strip()
    if not weight_str or not weight:
        return False, None, "Вес не может быть пустым"

    # Паттерн для валидации веса
    # (неотрицательное число, возможно с десятичной частью)
    pattern = r'^\d+([.]\d{1,2})?$'

    if not re.match(pattern, weight):
        return (
            False,
            None,
            "Некорректный формат веса. Используйте число (например: 20, 20.5)"
        )

    return True, float(weight), None


def validate_integer(
        value_str: str,
        field_name: str = "Значение"
        ) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация целого положительного числа.
    """
    if not value_str or not value_str.strip():
        return False, None, f"{field_name} не может быть пустым"

    # Паттерн для валидации целого числа
    pattern = r'^\d+$'

    if not re.match(pattern, value_str.strip()):
        return (
            False,
            None,
            f"Некорректный формат {field_name.lower()}. Нужно целое число"
        )

    try:
        value = int(value_str.strip())

        if value <= 0:
            return (
                False,
                None,
                f"{field_name} должно быть положительным числом"
            )

        return True, value, None
    except ValueError:
        return (
            False,
            None,
            f"Ошибка при преобразовании {field_name.lower()} в число"
        )


def validate_sets(sets_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация количества подходов.
    """
    return validate_integer(sets_str, "Количество подходов")


def validate_reps(reps_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация количества повторений.
    """
    return validate_integer(reps_str, "Количество повторений")


def validate_date(date_str: str) -> Tuple[
        bool, Optional[datetime], Optional[str]
        ]:
    """
    Валидация даты с использованием регулярных выражений.
    Поддерживает форматы: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY
    """
    if not date_str or not date_str.strip():
        return False, None, "Дата не может быть пустой"

    date_str = date_str.strip()

    # Паттерн для формата DD.MM.YYYY
    patterns = r'^\d{2}\.\d{2}\.\d{4}$'

    if not re.match(patterns, date_str):
        return False, None, "Некорректный формат даты. Используйте DD.MM.YYYY"

    # Проверяем, что дата может быть преобразована
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
        return True, date, None
    except ValueError:
        return (
            False,
            None,
            "Некорректный формат даты. Используйте DD.MM.YYYY"
        )


def validate_exercise_type(name: str) -> Tuple[
        bool, Optional[str], Optional[str]
        ]:
    """
    Валидация названия типа упражнения.
    """

    cleaned_name = name.strip()
    if not cleaned_name:
        return False, None, "Название упражнения не может быть пустым"

    # Проверка на длину
    if len(cleaned_name) < 1:
        return False, None, "Название упражнения слишком короткое"

    if len(cleaned_name) > 50:
        return (
            False,
            None,
            "Название упражнения слишком длинное (максимум 50 символов)"
        )

    # Проверка на разрешенные символы (буквы, цифры, пробелы, дефисы, подчерк.)
    if not re.match(r'^[а-яА-ЯёЁa-zA-Z0-9\s\-_]+$', cleaned_name):
        return False, None, "Название упражнения содержит недопустимые символы"

    return True, cleaned_name, None


def validate_comment(comment: str) -> str:
    """
    Валидация и очистка комментария.
    """
    if not comment:
        return ""

    cleaned_comment = comment.strip()

    # Ограничение длины комментария
    if len(cleaned_comment) > 200:
        cleaned_comment = cleaned_comment[:200]

    return cleaned_comment
