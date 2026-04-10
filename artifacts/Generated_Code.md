# Generated Code for Calculator


--- File: calculator.py ---
```python
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b
```

--- File: main.py ---
```python
#!/usr/bin/env python3
import sys
from calculator import add

def get_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError as e:
            print(f"Error: '{e.args[0]}' is not a valid number.")

def main() -> None:
    if len(sys.argv) == 3:
        try:
            num1 = float(sys.argv[1])
            num2 = float(sys.argv[2])
        except ValueError as e:
            print(f"Error: '{e.args[0]}' is not a valid number.")
            return
    else:
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
    result = add(num1, num2)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```