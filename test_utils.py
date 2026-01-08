"""
Проверяет поведение валидаторов: веса, целых чисел (подходы/повторы),
даты и типа упражнения.
"""

import unittest
from datetime import datetime

from utils import (
    validate_weight,
    validate_sets,
    validate_reps,
    validate_date,
    validate_exercise_type
)
from models import Exercise


class TestExercise(unittest.TestCase):
    """Тесты для класса Exercise."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.exercise_type = "Жим лежа"
        self.test_date = datetime(2024, 1, 15)

    def test_exercise_creation(self):
        """Тест создания упражнения."""
        exercise = Exercise(
            self.exercise_type, 80.0, 3, 10, self.test_date, "Тренировка"
        )
        self.assertEqual(exercise.exercise_type, "Жим лежа")
        self.assertEqual(exercise.weight, 80.0)
        self.assertEqual(exercise.sets, 3)
        self.assertEqual(exercise.reps, 10)
        self.assertEqual(exercise.date, self.test_date)
        self.assertEqual(exercise.comment, "Тренировка")


class TestUtilsValidators(unittest.TestCase):
    """Тесты для функций валидации в utils.py."""

    def test_validate_weight_valid_and_invalid(self):
        """Проверяет корректные/некорректные представления веса и границы"""
        ok, v, err = validate_weight("80")
        self.assertTrue(ok)
        self.assertEqual(v, 80.0)

        ok, v, err = validate_weight("80.5")
        self.assertTrue(ok)
        self.assertEqual(v, 80.5)

        ok, v, err = validate_weight("20.12")
        self.assertTrue(ok)
        self.assertEqual(v, 20.12)

        ok, v, err = validate_weight("20.123")
        self.assertFalse(ok)
        self.assertIsNone(v)
        self.assertIn("Некорректный формат веса", err)

        ok, v, err = validate_weight("")
        self.assertFalse(ok)
        self.assertIsNone(v)
        self.assertIn("не может быть пустым", err)

        ok, v, err = validate_weight("-5")
        self.assertFalse(ok)
        self.assertIn("Некорректный формат веса", err)

        ok, v, err = validate_weight(" 40 ")
        self.assertTrue(ok)
        self.assertEqual(v, 40.0)

    def test_validate_sets_reps_and_integer(self):
        """Проверяет значения подходов и повторений"""
        ok, val, err = validate_sets("3")
        self.assertTrue(ok)
        self.assertEqual(val, 3)

        ok, val, err = validate_sets("0")
        self.assertFalse(ok)

        ok, val, err = validate_sets(" 5 ")
        self.assertTrue(ok)
        self.assertEqual(val, 5)

        ok, val, err = validate_reps("10")
        self.assertTrue(ok)
        self.assertEqual(val, 10)

        ok, val, err = validate_reps("-1")
        self.assertFalse(ok)

        ok, val, err = validate_reps("3.5")
        self.assertFalse(ok)
        self.assertIn("целое число", err)

    def test_validate_date_formats_and_errors(self):
        """Проверяет корректный формат DD.MM.YYYY"""
        ok, dt, err = validate_date("01.02.2020")
        self.assertTrue(ok)
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.strftime("%d.%m.%Y"), "01.02.2020")

        ok, dt, err = validate_date("2020-01-01")
        self.assertFalse(ok)

        ok, dt, err = validate_date("31.02.2020")
        self.assertFalse(ok)

        ok, dt, err = validate_date("")
        self.assertFalse(ok)

    def test_validate_exercise_type_valid_and_invalid(self):
        """Проверяет приемлемые имена типов упражнений"""
        ok, name, err = validate_exercise_type("Жим")
        self.assertTrue(ok)
        self.assertEqual(name, "Жим")

        ok, name, err = validate_exercise_type(" Приседание 1 ")
        self.assertTrue(ok)
        self.assertEqual(name, "Приседание 1")

        ok, name, err = validate_exercise_type("планка-отжимание")
        self.assertTrue(ok)

        ok, name, err = validate_exercise_type("")
        self.assertFalse(ok)

        ok, name, err = validate_exercise_type("a" * 51)
        self.assertFalse(ok)

        ok, name, err = validate_exercise_type("Отжимания!")
        self.assertFalse(ok)


if __name__ == '__main__':
    unittest.main()
