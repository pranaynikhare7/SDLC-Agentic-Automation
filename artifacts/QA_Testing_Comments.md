# QA Testing Comments for Simple Calculator App

**Test Results**

| Test Case ID | Status | Feedback |
|--------------|--------|----------|
| **pytest – test_add** | Pass | `add(1, 2)` correctly returns `3`; `add(-1, 1)` correctly returns `0`. |
| **pytest – test_subtract** | Pass | `subtract(5, 3)` and `subtract(0, 5)` return the expected values. |
| **pytest – test_multiply** | Pass | `multiply(4, 5)` and `multiply(-2, 3)` produce the correct products. |
| **pytest – test_divide** | Pass | `divide(10, 2)` yields `5`; the `ZeroDivisionError` is correctly raised when the denominator is `0`. |
| **unittest – TestArithmeticFunctions.test_add** | **Fail** | Import error: `calculator` does not expose `OPS` or `VALID_OPS`. The test module fails to import, so this test never runs. |
| **unittest – TestArithmeticFunctions.test_subtract** | **Fail** | Same import error as above – the entire test module is skipped. |
| **unittest – TestArithmeticFunctions.test_multiply** | **Fail** | Same import error – test not executed. |
| **unittest – TestArithmeticFunctions.test_divide** | **Fail** | Same import error – test not executed. |
| **unittest – TestArithmeticFunctions.test_divide_with_float_denominator** | **Fail** | Same import error – test not executed. |
| **unittest – TestArithmeticFunctions.test_divide_negative_numbers** | **Fail** | Same import error – test not executed. |
| **unittest – test_calculator_unittest.py** | **Fail** | The file contains a syntax error – the `test_divide_negative_numbers` method is truncated (`self.assertEqual(divide(10` is incomplete). Even if this were fixed, the missing `OPS`/`VALID_OPS` definitions would still cause an ImportError. |

---

### Why the `unittest` tests are failing

1. **Missing Symbols**  
   The `calculator.py` module only defines the functions `add`, `subtract`, `multiply`, `divide`, `get_operand`, `get_operation`, and `main`. It does **not** expose `OPS` or `VALID_OPS`. The import line  
   ```python
   from calculator import add, subtract, multiply, divide, get_operand, get_operation, main, OPS, VALID_OPS
   ```  
   therefore raises an `ImportError` before any tests run.

2. **Syntax Error**  
   The `test_divide_negative_numbers` method is incomplete (`self.assertEqual(divide(10`), causing a `SyntaxError` that stops the test file from being parsed.

3. **Uncovered Interactive Functions**  
   The tests never exercise `get_operand`, `get_operation`, or `main`. While not a failure per se, this leaves a gap in coverage.

---

### Suggested Fixes

| Issue | Fix |
|-------|-----|
| **Missing `OPS` / `VALID_OPS`** | Either add the definitions to `calculator.py` (e.g. `OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}` and `VALID_OPS = set(OPS)`) **or** remove them from the import list in the test file. |
| **Syntax Error in Test File** | Complete the `test_divide_negative_numbers` method, e.g.:<br>`self.assertEqual(divide(10, 2), 5)`<br>`self.assertEqual(divide(-10, 2), -5)`<br>`self.assertEqual(divide(10, -2), -5)` |
| **Coverage of Interactive Functions** | Add unit tests that patch `builtins.input` and `builtins.print` to verify `get_operand`, `get_operation`, and `main`. Example:<br>`@patch('builtins.input', side_effect=['5', '2', '+'])\n@patch('builtins.print')\ndef test_main(self, mock_print, mock_input):\n    main()\n    mock_print.assert_called_with('Result: 7')` |
| **Consistent Test Naming** | Keep the test module names consistent (`test_calculator_pytest.py` vs. `test_calculator_unittest.py`) to avoid confusion. |
| **Documentation** | Add docstrings to the arithmetic functions to clarify expected input types and error conditions. |

---

### Updated `calculator.py` (minimal patch)

```python
#!/usr/bin/env python3
"""
Simple Calculator App
"""

def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero (or -0.0).
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b

def get_operand(prompt: str) -> float:
    """Prompt the user for a numeric operand, reprompting on invalid input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")

def get_operation() -> str:
    """Prompt the user to choose a valid operation symbol."""
    ops = {"+": add, "-": subtract, "*": multiply, "/": divide}
    while True:
        op = input("Select operation (+, -, *, /): ").strip()
        if op in ops:
            return op
        print("Invalid operation. Please choose from +, -, *, /.")

# Expose the operation mapping for external use (tests or other modules)
OPS = {"+": add, "-": subtract, "*": multiply, "/": divide}
VALID_OPS = set(OPS)

def main() -> None:
    """Run