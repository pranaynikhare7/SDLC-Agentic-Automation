# Generated Code for Simple Calculator App


# main.py
#!/usr/bin/env python3
from calculator import parse_input, calculate

def main():
    while True:
        try:
            line = input("calc> ").strip()
        except EOFError:
            break
        if line.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        tokens = line.split()
        if len(tokens) != 3:
            print("Error: Invalid input. Use: operand1 operator operand2")
            continue
        try:
            a, op, b = parse_input(tokens)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        result = calculate(a, op, b)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
    
# calculator.py
OPERATORS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else float("inf"),
}

def parse_input(tokens):
    a, op, b = tokens
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise ValueError("Operands must be numeric.")
    if op not in OPERATORS:
        raise ValueError("Unsupported operator.")
    if op == "/" and b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a, op, b

def calculate(a, op, b):
    return OPERATORS[op](a, b)