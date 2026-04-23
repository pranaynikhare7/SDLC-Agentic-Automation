# Test Cases for Simple Calculator App


```python
# test_calculator_unittest.py
"""
Unit‑tests for the `calculator` module using the standard unittest framework.
All public functions are exercised, including edge‑cases, error handling and
the interactive helper functions that use `input()`/`print()`.
"""

import math
import sys
import types
import unittest
from unittest.mock import patch, MagicMock

import calculator
from calculator import add, subtract, multiply, divide, get_operand, get_operation, main, OPS, VALID_OPS


class TestArithmeticFunctions(unittest.TestCase):
    """Pure functions – add, subtract, multiply, divide."""

    def test_add(self):
        # integer + integer
        self.assertEqual(add(1, 2), 3)
        # negative + positive
        self.assertEqual(add(-1, 1), 0)
        # float + float
        self.assertAlmostEqual(add(0.1, 0.2), 0.30000000000000004)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertAlmostEqual(subtract(0.3, 0.1), 0.19999999999999996)

    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(-2, 3), -6)
        # large numbers → overflow to inf
        self.assertTrue(math.isinf(multiply(1e308, 1e308)))

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(7, 3), 7 / 3)

        # Division by zero
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)
        with self.assertRaises(ZeroDivisionError):
            divide(5, -0.0)

        # Very small denominator → huge result (may become inf)
        self.assertTrue(math.isinf(divide(1e308, 1e-308)))

    def test_divide_with_float_denominator(self):
        self.assertAlmostEqual(divide(1.5, 0.5), 3.0)

    def test_divide_negative_numbers(self):
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10