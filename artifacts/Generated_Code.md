# Generated Code for Simple Calculator App


```python
# calculator_module.py
class Calculator:
    def __init__(self):
        pass

    def add(self, num1, num2):
        return num1 + num2

    def subtract(self, num1, num2):
        return num1 - num2

    def multiply(self, num1, num2):
        return num1 * num2

    def divide(self, num1, num2):
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return num1 / num2
```

```python
# app.py
from flask import Flask, request, jsonify
from calculator_module import Calculator

app = Flask(__name__)
calculator = Calculator()

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    operation = data['operation']

    if operation == 'add':
        result = calculator.add(num1, num2)
    elif operation == 'subtract':
        result = calculator.subtract(num1, num2)
    elif operation == 'multiply':
        result = calculator.multiply(num1, num2)
    elif operation == 'divide':
        try:
            result = calculator.divide(num1, num2)
        except ZeroDivisionError as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Invalid operation'}), 400

    return jsonify({'result': result})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
```

```python
# requirements.txt
Flask
```

```python
# Dockerfile
FROM python:3.9-slim

# Set working directory to /app
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .
COPY calculator_module.py .

# Expose port
EXPOSE 5000

# Run command
CMD ["python", "app.py"]
```

```yml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calculator-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: calculator-app
  template:
    metadata:
      labels:
        app: calculator-app
    spec:
      containers:
      - name: calculator-app
        image: calculator-app:latest
        ports:
        - containerPort: 5000
```

```python
# security_config.py
import os

class SecurityConfig:
    def __init__(self):
        self.secret_key = os.environ.get('SECRET_KEY')
```

```bash
# Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t calculator-app:latest .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
```