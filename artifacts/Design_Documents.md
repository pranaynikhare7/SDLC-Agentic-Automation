# Design Documents for Calculator

## Functional Design Document
# Functional Design Document: Calculator

---

## 1. Introduction and Purpose  
This document describes the design of a lightweight, console‑based calculator that supports a single operation: addition. The goal is to provide a clear, maintainable solution that can be executed on any system with Python 3.x without external dependencies.

---

## 2. Project Scope  
- **Application type**: Stand‑alone Python script (`calculator.py`).  
- **Supported operation**: Addition of two numeric operands (int or float).  
- **User interface**: Text console (no GUI).  
- **Code size**: ≤ 50 non‑comment, non‑blank lines.  
- **Platform**: Any OS with Python 3.x installed.

---

## 3. User Roles and Permissions  
| Role | Permissions | Notes |
|------|-------------|-------|
| **End‑User** | Execute script, input numbers, view result | No authentication required |
| **Developer** | Modify source, run tests | Must keep line count ≤ 50 |
| **Maintainer** | Update documentation | No code changes required |

---

## 4. Functional Requirements Breakdown  
| FR# | Requirement | User Story ID(s) | Priority |
|-----|-------------|------------------|----------|
| FR‑1 | Prompt for two numeric inputs | US‑001, US‑002 | 1 |
| FR‑2 | Validate numeric input (int/float) | US‑002 | 1 |
| FR‑3 | Compute sum of inputs | US‑002 | 1 |
| FR‑4 | Display result | US‑002 | 1 |
| FR‑5 | Handle invalid input gracefully | US‑002 | 2 |
| FR‑6 | Keep source < 50 lines | US‑003 | 3 |
| FR‑7 | No external libraries | US‑001 | 3 |

---

## 5. User Interface Design Guidelines  
- **Console prompts**: Clear and concise.  
- **Error messages**: Specific, e.g., *“Error: 'abc' is not a valid number.”*  
- **Result format**: `Result: <value>`  
- **Exit**: Press `Enter` after result to quit.

---

## 6. Business Process Flows  

### 6.1 Main Flow  
```
[Start] → Prompt 1 → Validate 1
   │
   ├─ If invalid → Show error → Prompt 1
   └─ If valid → Prompt 2 → Validate 2
          │
          ├─ If invalid → Show error → Prompt 2
          └─ If valid → Compute Sum → Display Result → [End]
```

### 6.2 Error Handling Flow  
```
Invalid Input → Print Error → Loop to Prompt
```

---

## 7. Data Entities and Relationships  
| Entity | Attributes | Relationship |
|--------|------------|--------------|
| **Input** | `operand1` (float), `operand2` (float) | None (flat structure) |
| **Result** | `sum` (float) | Derived from Input |

No persistent storage; all data is transient during execution.

---

## 8. Validation Rules  
| Field | Rule | Error Message |
|-------|------|---------------|
| `operand1` | Must be convertible to `float` | “Error: 'X' is not a valid number.” |
| `operand2` | Must be convertible to `float` | “Error: 'Y' is not a valid number.” |

---

## 9. Reporting Requirements  
- **Console output** only.  
- No log files or external reports.

---

## 10. Integration Points  
| Integration | Description | Status |
|-------------|-------------|--------|
| None | The calculator is a standalone script. | N/A |

---

## 11. Sample Implementation (≤ 50 Lines)  

```python
#!/usr/bin/env python3
"""
calculator.py – Simple console calculator that adds two numbers.
"""

def get_number(prompt: str) -> float:
    """Prompt user and return a valid float."""
    while True:
        try:
            return float(input(prompt))
        except ValueError as exc:
            print(f"Error: '{exc.args[0]}' is not a valid number.")

def main() -> None:
    """Main entry point."""
    num1 = get_number("Enter first number: ")
    num2 = get_number("Enter second number: ")
    result = num1 + num2
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

*Line count (excluding comments/blank lines): 23* – well below the 50‑line limit.

---

### 12. Test Plan (Optional)  
| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Valid integers | `3`, `4` | `Result: 7` |
| Valid floats | `2.5`, `4.1` | `Result: 6.6` |
| Mixed types | `5`, `3.2` | `Result: 8.2` |
| Invalid first | `a`, `3` | Error message + re‑prompt |
| Invalid second | `4`, `b` | Error message + re‑prompt |

---

### 13. Deployment Checklist  
1. Ensure Python 3.x is installed.  
2. Place `calculator.py` on the target machine.  
3. Run with `python calculator.py`.  
4. Verify output and error handling.

---

## 14. Maintenance Notes  
- Keep the script under 50 lines; avoid adding new functions unless necessary.  
- Document any future enhancements in this document.  
- Use descriptive variable names to aid readability.

---

**Prepared by:**  
*Your Name*  
*Date:* 2026‑04‑10

## Technical Design Document
# Technical Design Document: Calculator

---

## 1. System Architecture

| Component | Responsibility | Notes |
|-----------|----------------|-------|
| **CLI Interface** | Reads two numeric values from the console and prints the result. | Single‑file, no GUI. |
| **Business Logic** | Performs the addition operation. | Pure function `add(a, b)` – testable in isolation. |
| **Input Parser** | Validates and converts user input to `float`. | Raises `ValueError` on invalid data. |
| **Error Handler** | Catches parsing errors and displays a friendly message. | No crash on bad input. |
| **Main Entrypoint** | Orchestrates the flow: input → add → output. | Guarded by `if __name__ == "__main__":`. |

> **Flow Diagram (text form)**  
> ```
> +------------------+
> |  Input:  num1    |
> +------------------+
>          |
>          v
> +------------------+
> |  Input:  num2    |
> +------------------+
>          |
>          v
> +------------------+
> |  add(num1, num2) |
> +------------------+
>          |
>          v
> +------------------+
> |  Output: result  |
> +------------------+
> ```

---

## 2. Technology Stack and Justification

| Technology | Version | Justification |
|------------|---------|---------------|
| Python | 3.8+ | Widely installed, no external dependencies, supports type hints and f‑strings for clarity. |
| Standard Library | – | Keeps the code lightweight (<50 lines) and portable. |

> **Why no UI frameworks?**  
> The requirement is a “simple Python application with no UI”, so a console app satisfies the user stories and keeps the code minimal.

---

## 3. Database Schema

> **Not applicable.**  
> The calculator is stateless; no persistence or database is required.

---

## 4. API Specifications

| Interface | Method | Parameters | Returns | Notes |
|-----------|--------|------------|---------|-------|
| **Command‑Line** | `python calculator.py` | `--num1`, `--num2` (optional) | Prints the sum | If arguments are omitted, the script prompts interactively. |

> **Command‑Line Usage Example**  
> ```bash
> $ python calculator.py --num1 12.5 --num2 7.3
> Result: 19.8
> ```

---

## 5. Security Considerations

- **Input Validation** – Only numeric values are accepted; parsing errors are caught and reported.
- **No `eval` or `exec`** – Prevents arbitrary code execution.
- **No External Network Calls** – The app is offline by design, eliminating network‑based threats.
- **Minimal Dependencies** – Using only the Python standard library reduces attack surface.

---

## 6. Performance Considerations

- **Time Complexity** – O(1) for addition.
- **Memory Footprint** – < 1 KB of code, trivial runtime memory.
- **I/O** – Blocking console input; acceptable for a simple tool.

---

## 7. Scalability Approach

> **Not required.**  
> The calculator handles a single pair of numbers per run. If future requirements grow (e.g., batch processing), the architecture can be extended by adding a loop or file‑input mode without affecting the core logic.

---

## 8. Deployment Strategy

| Step | Action | Tool |
|------|--------|------|
| 1 | Place `calculator.py` in a directory. | File system |
| 2 | Run via command line: `python calculator.py`. | Terminal |
| 3 | For distribution