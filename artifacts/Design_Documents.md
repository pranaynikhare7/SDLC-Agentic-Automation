# Design Documents for Simple Calculator App

## Functional Design Document
# Functional Design Document: Simple Calculator App

---

## 1. Overview and Objectives

| Item | Description |
|------|-------------|
| **Project Name** | Simple Calculator App |
| **Purpose** | Deliver a lightweight, pure‑Python command‑line calculator that performs basic arithmetic (addition, subtraction, multiplication, division) with a clean, maintainable codebase. |
| **Key Constraints** | < 70 lines of code, no external libraries, single‑file executable, clear CLI, graceful error handling. |
| **Target Environment** | Any standard Python 3.x interpreter (3.6+). No additional runtime dependencies. |

---

## 2. Scope Definition

| Scope | Description | Out‑of‑Scope |
|-------|-------------|--------------|
| **In‑Scope** | • Two‑operand arithmetic (binary operations).<br>• Command‑line interface with prompt.<br>• Input validation and error messaging.<br>• Inline documentation and concise README. | • GUI or web interface.<br>• Persistence or history feature.<br>• Advanced math functions (exponentiation, trigonometry). |

---

## 3. Roles and Access Control

| Role | Responsibilities |
|------|------------------|
| **Developer** | Write, test, and maintain the Python script. |
| **Tester** | Verify functional requirements, line‑count, and error handling. |
| **End‑User** | Interact with the CLI to perform calculations. |

> **Access Control** – The application is self‑contained; no authentication or user permissions are required.

---

## 4. Functional Requirements Analysis

| US ID | Title | Requirement | Acceptance Criteria |
|-------|-------|-------------|---------------------|
| **US‑001** | Simple Python Application | • Pure Python, single‑file executable.<br>• Supports +, –, *, ÷ for two operands.<br>• User‑friendly CLI.<br>• Graceful error handling.<br>• Well‑commented code & README. | • Runs with `python calc.py`.<br>• All four operations work with integer or float operands.<br>• Invalid input shows a helpful message.<br>• README explains usage. |
| **US‑002** | Maintain Code Size Under 70 Lines | • Total lines ≤ 70.<br>• No external imports.<br>• Only essential inline comments. | • Manual or script count ≤ 70.<br>• No external modules used. |

### Functional Requirement Mapping

| Feature | US‑001 | US‑002 |
|---------|--------|--------|
| CLI Prompt | ✅ | ✅ |
| Binary Operations | ✅ | ✅ |
| Input Parsing | ✅ | ✅ |
| Error Handling | ✅ | ✅ |
| Documentation | ✅ | ✅ |
| Line Count | ✅ | ✅ |

---

## 5. User Interface and Experience Guidelines

* **Interface Type** – Command‑line (terminal/console).  
* **Prompt Format** – `calc> `  
* **Input Syntax** – `operand1 operator operand2` (e.g., `12 + 7`).  
* **Supported Operators** – `+`, `-`, `*`, `/`.  
* **Feedback** – Result or error message printed on the same line.  
* **Exit** – User can type `quit` or `exit` to terminate.

```text
calc> 12 + 7
Result: 19

calc> 5 / 0
Error: Division by zero is not allowed.

calc> quit
Goodbye!
```

*All messages are concise and free of jargon.*

---

## 6. Business Workflow Processes

1. **Start** – User launches `calc.py`.  
2. **Prompt** – Application displays `calc> `.  
3. **Input** – User enters expression or exit command.  
4. **Parse** – Split input into operands and operator.  
5. **Validate** – Ensure two operands and a supported operator; check division by zero.  
6. **Compute** – Perform arithmetic using Python’s built‑in operators.  
7. **Display** – Show `Result:` or `Error:` message.  
8. **Loop** – Return to step 2 until exit command.  
9. **End** – Print farewell message and terminate.

---

## 7. Data Model and Relationships

| Entity | Attributes | Notes |
|--------|------------|-------|
| **Calculation** | `operand1` (float), `operator` (str), `operand2` (float) | Simple tuple; no persistence. |
| **Result** | `value` (float) | Returned to the user. |

> *No relational database or external storage is involved.*

---

## 8. Data Validation and Business Rules

| Rule | Description | Handling |
|------|-------------|----------|
| **Operand Count** | Exactly two numeric operands required. | Prompt error: “Invalid input: expected two numbers.” |
| **Operator Validity** | Only `+`, `-`, `*`, `/` allowed. | Prompt error: “Unsupported operator.” |
| **Division by Zero** | `operand2` cannot be zero when operator is `/`. | Prompt error: “Division by zero is not allowed.” |
| **Numeric Parsing** | Operands must parse to `float`. | Prompt error: “Operands must be numeric.” |
| **Whitespace Robustness** | Accept arbitrary spaces between tokens. | Strip and split on whitespace. |

---

## 9. Reporting and Analytics Requirements

| Feature | Description |
|---------|-------------|
| **Operation Log** | Optional console log of each calculation (enabled via a `--log` flag). |
| **Usage Stats** | Not required; the app remains stateless. |

> *Given the simplicity, no persistent reporting is implemented.*

---

## 10. System Integrations and Interfaces

| Integration | Interface | Notes |
|-------------|-----------|-------|
| **Python Runtime** | Standard library only. | The script relies solely on built‑in functions (`input()`, `print()`, `float()`). |
| **External Tools** | None. | No external APIs or services. |

---

## Appendix: Sample Code Skeleton (≤ 70 Lines)

```python
#!/usr/bin/env python3
"""
Simple Calculator App
Author: <Your Name>
"""

OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else None,
}

def parse_input(line):
    """Return (operand1, operator, operand2) or None on error."""
    tokens = line.strip().split()
    if len(tokens) != 3:
        return None
    try:
        a, op, b = float(tokens[0]), tokens[1], float(tokens[2])
    except ValueError:
        return None
    if op not in OPERATORS:
        return None
    return a, op, b

def calculate(a, op, b):
    """Return result or error string."""
    if op == '/' and b == 0:
        return "Error: Division by zero."
    try:
        return f"Result: {OPERATORS[op](a, b)}"
    except Exception as e:
        return f"Error: {e}"

def main():
    while True:
        try:
            line = input("calc> ").strip()
        except EOFError:
            break
        if line.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        parsed = parse_input(line)
        if not parsed:
            print("Error: Invalid input. Use: operand1 operator operand2")
            continue
        a, op, b = parsed
        print(calculate(a, op, b))

if __name__ == "__main__":
    main()
```

> **Line Count** – 55 lines (including comments).  
> **Dependencies** – None beyond Python standard library.  

---

### README Outline

```
# Simple Calculator App

## Description
Lightweight command‑line calculator performing +, -, *, / on two operands.

## Requirements
- Python 3.6 or newer

## Usage
```bash
$ python calc.py

## Technical Design Document
# Technical Design Document: Simple Calculator App

> **Purpose** – This document describes the design of a lightweight, pure‑Python calculator that supports the four basic arithmetic operations.  
> **Scope** – The application is a single‑file command‑line tool that must stay under 70 lines of code, run on any standard Python 3.x environment, and provide clear, user‑friendly interaction.

---

## 1. System Architecture Overview

```
+----------------+          +---------------------+          +-----------------+
|   User Input   |  --->    |  Command‑Line Parser|  --->    |  Calculator Core|
+----------------+          +---------------------+          +-----------------+
        |                            |                          |
        |                            v                          v
        |                     +----------------+     +-----------------+
        |                     |   Error Handler|     |   Result Printer|
        |                     +----------------+     +-----------------+
```

* **User Input** – Raw text entered by the user.  
* **Command‑Line Parser** – Tokenizes and validates the input.  
* **Calculator Core** – Performs arithmetic logic.  
* **Error Handler** – Catches and reports invalid operations.  
* **Result Printer** – Formats and displays the output.

The entire stack resides in one Python module (`calculator.py`), ensuring minimal footprint and zero external dependencies.

---

## 2. Technology Stack and Rationale

| Component | Technology | Why |
|-----------|------------|-----|
| Runtime | Python 3.8+ (standard library only) | Widely available, readable syntax, built‑in `argparse` for CLI. |
| Build | `setup.py` (optional) | Enables `pip install .` for reproducible environments. |
| Testing | `unittest` | Standard library, no extra installs. |
| Linting | `flake8` (optional) | Enforces line‑count and style constraints. |
| Packaging | `zipapp` (optional) | Create a single executable archive. |

*No external dependencies* keeps the application portable and trivial to deploy.

---

## 3. Data Model and Schema Design

The calculator only handles two numeric operands and an operator. The data model can be represented as a simple tuple:

| Field | Type | Description |
|-------|------|-------------|
| `operand1` | `float` | First numeric value |
| `operand2` | `float` | Second numeric value |
| `operator` | `str` | One of `+`, `-`, `*`, `/` |

```python
# Example data structure
operation = (operand1, operator, operand2)
```

No persistent storage is required; all data is transient.

---

## 4. API Design and Specifications

Although the calculator is a CLI tool, its internal API is defined by three public functions:

| Function | Signature | Description |
|----------|-----------|-------------|
| `parse_input(arg_list: List[str]) -> Tuple[float, str, float]` | Parses CLI arguments into operands and operator. |
| `calculate(op1: float, operator: str, op2: float) -> float` | Executes the arithmetic operation. |
| `main() -> None` | Entry point; orchestrates parsing, calculation, error handling, and output. |

### Function Details

```python
def parse_input(args: List[str]) -> Tuple[float, str, float]:
    """
    Expects three arguments: operand1, operator, operand2.
    Raises ValueError on invalid format or unsupported operator.
    """
    ...

def calculate(op1: float, operator: str, op2: float) -> float:
    """
    Performs the operation and handles division by zero.
    """
    ...

def main() -> None:
    """
    Parses sys.argv, invokes calculate(), and prints the result.
    """
    ...
```

*All functions are pure and have no side effects except for `main()`, which interacts with the console.*

---

## 5. Security Architecture and Controls

| Threat | Mitigation |
|--------|------------|
| **Injection via malformed input** | Strict parsing; only numeric values and a whitelist of operators are accepted. |
| **Denial‑of‑Service via large numbers** | Python’s `float` handles arbitrary size; no explicit limits required. |
| **Arbitrary code execution** | No `eval` or `exec`; all logic is static. |
| **Information leakage** | Errors are generic; no stack traces are exposed to the user. |

The application runs with the least privileges required—no file writes, no network access.

---

## 6. Performance Optimization Strategies

| Area | Technique | Rationale |
|------|-----------|-----------|
| **Parsing** | Use `argparse` for robust, fast argument parsing. | Built‑in C implementation. |
| **Computation** | Simple arithmetic operators (`+`, `-`, `*`, `/`). | Constant‑time operations. |
| **Memory** | No data persistence; all variables are short‑lived. | Minimal heap usage. |
| **Startup** | Single file; no import cycles. | < 0.1 s startup on modern hardware. |

Given the trivial workload, micro‑optimizations are unnecessary; the focus is on clarity and reliability.

---

## 7. Scalability and Reliability Approach

* **Scalability** – The application is stateless and single‑threaded; scaling horizontally is not applicable.  
* **Reliability** – Comprehensive unit tests cover all four operations, division by zero, and invalid input scenarios.  
* **Error Recovery** – Graceful exit codes (`0` for success, `1` for error) allow scripts to detect failures.

---

## 8. Deployment and Release Strategy

1. **Source Distribution** – Provide a single `calculator.py`.  
2. **Executable Archive** – Optionally build with `python -m zipapp calculator.py -o calculator.pyz`.  
3. **Installation** – Users can run `python calculator.py` or `python calculator.pyz`.  
4. **Versioning** – Semantic versioning (e.g., `v1.0.0`).  
5. **Release Notes** – Include change log in `CHANGELOG.md`.

*No CI/CD pipeline is required for such a small project, but a simple GitHub Actions workflow can run tests and verify line count.*

---

## 9. External Integrations and Dependencies

| Integration | Status | Notes |
|-------------|--------|-------|
| External libraries | **None** | Only Python standard library is used. |
| CI/CD | Optional | GitHub Actions can run `flake8` and `unittest`. |
| Packaging | `zipapp` (optional) | Allows single‑file distribution. |

---

## 10. Environment Setup (Development, Testing, Production)

| Environment | Configuration | Commands |
|-------------|---------------|----------|
| **Development** | Python 3.8+ installed | `pip install -r requirements.txt` (if any) |
| **Testing** | Same as dev; run tests | `python -m unittest discover tests` |
| **Production** | Any machine with Python 3.8+ | `python calculator.py <op1> <operator> <op2>` |

### Sample `calculator.py` (≤ 70 lines)

```python
#!/usr/bin/env python3
"""
Simple Calculator – Performs +, -, *, / on two numeric operands.
Usage: python calculator.py <operand1> <operator> <operand2>
"""

import sys

OPERATORS = {"+": lambda a, b: a + b,
             "-": lambda a, b: a - b,
             "*": lambda a, b: a * b,
             "/": lambda a, b: a / b if b != 0 else float('inf')}

def parse_input(args):
    if len(args) != 3:
        raise ValueError("Exactly three arguments required.")
    op1, oper, op2 = args
    if oper not in OPERATORS:
        raise ValueError(f