# Test Cases for Simple Calculator App


```python
import unittest
from calculator_module import Calculator
import json
from app import app

class TestCalculatorModule(unittest.TestCase):

    def test_add(self):
        calculator = Calculator()
        self.assertEqual(calculator.add(10, 5), 15)
        self.assertEqual(calculator.add(-10, 5), -5)
        self.assertEqual(calculator.add(-10, -5), -15)

    def test_subtract(self):
        calculator = Calculator()
        self.assertEqual(calculator.subtract(10, 5), 5)
        self.assertEqual(calculator.subtract(-10, 5), -15)
        self.assertEqual(calculator.subtract(-10, -5), -5)

    def test_multiply(self):
        calculator = Calculator()
        self.assertEqual(calculator.multiply(10, 5), 50)
        self.assertEqual(calculator.multiply(-10, 5), -50)
        self.assertEqual(calculator.multiply(-10, -5), 50)

    def test_divide(self):
        calculator = Calculator()
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertEqual(calculator.divide(-10, 2), -5)
        self.assertEqual(calculator.divide(-10, -2), 5)
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(10, 0)

class TestApp(unittest.TestCase):

    def test_calculate_add(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 5, 'operation': 'add'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'], 15)

    def test_calculate_subtract(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 5, 'operation': 'subtract'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'], 5)

    def test_calculate_multiply(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 5, 'operation': 'multiply'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'], 50)

    def test_calculate_divide(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 2, 'operation': 'divide'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['result'], 5)

    def test_calculate_divide_by_zero(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 0, 'operation': 'divide'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Cannot divide by zero')

    def test_calculate_invalid_operation(self):
        tester = app.test_client()
        data = {'num1': 10, 'num2': 5, 'operation': 'invalid'}
        response = tester.post('/calculate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Invalid operation')

    def test_healthcheck(self):
        tester = app.test_client()
        response = tester.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
```
This test suite covers the following scenarios:

1.  **Calculator Module Tests**:

    *   Test the `add`, `subtract`, `multiply`, and `divide` methods of the `Calculator` class with different input values, including positive and negative numbers.
    *   Test the `divide` method with a divisor of zero to ensure it raises a `ZeroDivisionError`.
2.  **App Tests**:

    *   Test the `/calculate` endpoint with different operations (`add`, `subtract`, `multiply`, and `divide`) and input values.
    *   Test the `/calculate` endpoint with an invalid operation to ensure it returns an error response.
    *   Test the `/calculate` endpoint with a division by zero to ensure it returns an error response.
    *   Test the `/healthcheck` endpoint to ensure it returns a healthy status.

By running these tests, you can ensure the correctness and reliability of the calculator application.