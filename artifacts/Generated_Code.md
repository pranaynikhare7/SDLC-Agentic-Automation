# Generated Code for Simple Calculator App


```python
# calculator.py
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero."
    return x / y

def validate_input(user_input):
    try:
        x, operator, y = user_input.split()
        return float(x), operator, float(y)
    except ValueError:
        return None, None, None
```

```python
# main.py
from calculator import add, subtract, multiply, divide, validate_input

def main():
    while True:
        user_input = input("Enter operation (or 'quit' to exit): ")

        if user_input.lower() == 'quit':
            print("Exiting the calculator.")
            break

        x, operator, y = validate_input(user_input)
        if x is None or operator is None or y is None:
            print("Error: Invalid input. Please use format 'x operator y'.")
            continue

        if operator == '+':
            print(f"Result: {add(x, y)}")
        elif operator == '-':
            print(f"Result: {subtract(x, y)}")
        elif operator == '*':
            print(f"Result: {multiply(x, y)}")
        elif operator == '/':
            print(f"Result: {divide(x, y)}")
        else:
            print("Error: Unknown operator.")

if __name__ == "__main__":
    main()
```

```python
# README.md
# Simple Calculator App

This is a simple command-line calculator application that allows users to perform basic arithmetic operations such as addition, subtraction, multiplication, and division.

## Usage

To run the calculator, simply execute the `main.py` script. You can input calculations directly in the format `x operator y` (e.g., `2 + 3`). To exit the application, type `quit`.

## Functions

- `add(x, y)`: Returns the sum of x and y.
- `subtract(x, y)`: Returns the difference of x and y.
- `multiply(x, y)`: Returns the product of x and y.
- `divide(x, y)`: Returns the quotient of x and y, handling division by zero.

## Requirements

Ensure you have Python installed on your system to run this application.
```

```python
# tests.py
import unittest
from calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, 15), -5)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 5), -5)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(5, 0), "Error: Division by zero.")

if __name__ == '__main__':
    unittest.main()
```