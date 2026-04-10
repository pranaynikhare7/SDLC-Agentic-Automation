# Test Cases for Calculator


```python
# tests/test_calculator_and_main.py
"""
Unit tests for the tiny calculator and CLI entry point.
All tests are written using the standard unittest framework.
"""

import sys
import builtins
import io
import unittest
from unittest import mock
from contextlib import redirect_stdout

# Import the modules under test
import calculator
import main


class TestAddFunction(unittest.TestCase):
    """Positive & negative tests for calculator.add."""

    def test_add_positive_numbers(self):
        self.assertEqual(calculator.add(1.2, 3.4), 4.6)

    def test_add_negative_numbers(self):
        self.assertEqual(calculator.add(-1.5, -2.5), -4.0)

    def test_add_zero(self):
        self.assertEqual(calculator.add(0.0, 0.0), 0.0)

    def test_add_negative_zero(self):
        # -0.0 + 0.0 should be 0.0
        self.assertEqual(calculator.add(-0.0, 0.0), 0.0)

    def test_add_large_numbers(self):
        # 1e308 + 1e308 overflows to inf
        result = calculator.add(1e308, 1e308)
        self.assertTrue(result == float("inf"))

    def test_add_precision(self):
        # Floating point arithmetic is not exact
        self.assertAlmostEqual(calculator.add(0.1, 0.2), 0.3, places=7)


class TestGetNumberFunction(unittest.TestCase):
    """Tests for main.get_number, covering normal, invalid, and edge cases."""

    @mock.patch.object(builtins, "input", return_value="5.5")
    def test_get_number_valid_input(self, mock_input):
        self.assertEqual(main.get_number("prompt: "), 5.5)
        mock_input.assert_called_once_with("prompt: ")

    @mock.patch.object(builtins, "input", side_effect=["abc", "3.3"])
    def test_get_number_invalid_then_valid(self, mock_input):
        # First call raises ValueError, second call returns valid float
        with io.StringIO() as buf, redirect_stdout(buf):
            result = main.get_number("prompt: ")
            output = buf.getvalue()
        self.assertEqual(result, 3.3)
        self.assertIn("Error:", output)  # Error message printed
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch.object(builtins, "input", side_effect=["", "2"])
    def test_get_number_empty_then_valid(self, mock_input):
        with io.StringIO() as buf, redirect_stdout(buf):
            result = main.get_number("prompt: ")
            output = buf.getvalue()
        self.assertEqual(result, 2.0)
        self.assertIn("Error:", output)

    @mock.patch.object(builtins, "input", side_effect=EOFError)
    def test_get_number_eof_propagates(self, mock_input):
        # Original implementation does not catch EOFError; it should propagate
        with self.assertRaises(EOFError):
            main.get_number("prompt: ")

    @mock.patch.object(builtins, "input", side_effect=KeyboardInterrupt)
    def test_get_number_keyboard_interrupt_propagates(self, mock_input):
        with self.assertRaises(KeyboardInterrupt):
            main.get_number("prompt: ")


class TestMainFunction(unittest.TestCase):
    """Tests for main.main, covering CLI arguments, interactive mode, and error handling."""

    def run_main_with_args(self, argv, inputs=None):
        """
        Helper to run main.main with a specific sys.argv list.
        Optionally patch builtins.input with a list of responses.
        Returns captured stdout and any exception raised.
        """
        with mock.patch.object(sys, "argv", argv):
            if inputs is not None:
                input_patch = mock.patch.object(builtins, "input", side_effect=inputs)
                input_patch.start()
            else:
                input_patch = None
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    main.main()
                except Exception as e:
                    exc = e
                else:
                    exc = None
