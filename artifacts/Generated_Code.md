# Generated Code for Simple Calculator App


# calculator.py
```python
#!/usr/bin/env python3
"""
Simple Calculator App
"""

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b

def get_operand(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")

def get_operation() -> str:
    ops = {"+": add, "-": subtract, "*": multiply, "/": divide}
    while True:
        op = input("Select operation (+, -, *, /): ").strip()
        if op in ops:
            return op
        print("Invalid operation. Please choose from +, -, *, /.")

def main() -> None:
    a = get_operand("Enter first number: ")
    b = get_operand("Enter second number: ")
    op = get_operation()
    ops = {"+": add, "-": subtract, "*": multiply, "/": divide}
    try:
        result = ops[op](a, b)
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: Division by zero")

if __name__ == "__main__":
    main()
```

# test_calculator.py
```python
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(4, 5) == 20
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
```