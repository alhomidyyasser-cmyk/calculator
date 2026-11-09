import unittest
from unittest.mock import Mock

from main2 import CalculatorApp, SafeCalculator


class SafeCalculatorTests(unittest.TestCase):
    def test_calculates_supported_expressions(self):
        examples = {
            "2 + 3 * 4": 14.0,
            "2^3": 8.0,
            "sqrt(81)": 9.0,
            "sin(pi / 2)": 1.0,
            "log(100)": 2.0,
            "10 % 3": 1.0,
        }
        for expression, expected in examples.items():
            with self.subTest(expression=expression):
                self.assertEqual(SafeCalculator.calculate(expression), expected)

    def test_rejects_empty_unsupported_and_non_finite_results(self):
        for expression in ("", "True", "__import__('os')", "1e308 * 1e308"):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    SafeCalculator.calculate(expression)

    def test_division_by_zero_is_reported(self):
        with self.assertRaises(ZeroDivisionError):
            SafeCalculator.calculate("1 / 0")


class CalculatorAppTests(unittest.TestCase):
    def test_reuses_newest_history_entry_at_top_of_list(self):
        app = CalculatorApp.__new__(CalculatorApp)
        app.history = [("3 + 3", "6"), ("2 + 2", "4")]
        app.history_box = Mock()
        app.history_box.curselection.return_value = (0,)
        app.expression = Mock()
        app.display = Mock()
        app.status = Mock()

        app._reuse_history(Mock())

        app.expression.set.assert_called_once_with("6")

    def test_memory_does_not_store_a_non_finite_value(self):
        app = CalculatorApp.__new__(CalculatorApp)
        app.memory = 1e308
        app.expression = Mock()
        app.expression.get.return_value = "1e308"
        app.status = Mock()
        app.bell = Mock()

        app._memory("add")

        self.assertEqual(app.memory, 1e308)
        app.bell.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
