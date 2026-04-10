# Generated Code for Calculator


```python
# calculator.py

def add_numbers(num1, num2):
    return num1 + num2

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("Simple Calculator for Addition")
    num1 = get_number("Enter the first number: ")
    num2 = get_number("Enter the second number: ")
    
    result = add_numbers(num1, num2)
    print(f"The sum is: {result}")

if __name__ == "__main__":
    main()
``` 

This single file encapsulates all the required functionality for the calculator application adhering to the constraints specified.