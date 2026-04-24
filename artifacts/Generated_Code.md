# Generated Code for Simple Calculator


```plaintext
calculator.py
```
```python
class Calculator:
    def add(self, operands):
        return sum(operands)

    def subtract(self, operands):
        return operands[0] - operands[1]

    def multiply(self, operands):
        result = 1
        for num in operands:
            result *= num
        return result

    def divide(self, operands):
        if operands[1] == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return operands[0] / operands[1]
```

```plaintext
input_handler.py
```
```python
class InputHandler:
    @staticmethod
    def validate_inputs(operands):
        if len(operands) != 2:
            raise ValueError("Exactly two operands are required.")
        for operand in operands:
            if not isinstance(operand, (int, float)):
                raise ValueError(f"Invalid operand: {operand}. Operands must be numeric.")
```

```plaintext
main.py
```
```python
from calculator import Calculator
from input_handler import InputHandler

def main():
    calc = Calculator()

    while True:
        operation = input("Enter operation (add, subtract, multiply, divide) or 'exit' to quit: ")
        
        if operation == 'exit':
            break
        
        try:
            operands = list(map(float, input("Enter two numbers separated by space: ").split()))
            InputHandler.validate_inputs(operands)

            if operation == 'add':
                print("Result:", calc.add(operands))
            elif operation == 'subtract':
                print("Result:", calc.subtract(operands))
            elif operation == 'multiply':
                print("Result:", calc.multiply(operands))
            elif operation == 'divide':
                print("Result:", calc.divide(operands))
            else:
                print("Invalid operation.")
        
        except ValueError as e:
            print("Error:", e)
        except ZeroDivisionError as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
```

```plaintext
test_calculator.py
```
```python
import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add([1, 2]), 3)
        self.assertEqual(self.calc.add([-1, 1]), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract([5, 3]), 2)
        self.assertEqual(self.calc.subtract([0, 0]), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply([3, 4]), 12)
        self.assertEqual(self.calc.multiply([5, 0]), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide([10, 2]), 5)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide([1, 0])

if __name__ == "__main__":
    unittest.main()
```