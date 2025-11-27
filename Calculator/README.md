# Advanced Calculator

A secure calculator with advanced mathematical functions built with Python and Tkinter.

## Features

- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Advanced Functions**:
  - Trigonometric: sin, cos, tan
  - Logarithm: log
  - Square root: √
  - Power: ^
  - Constants: π (pi), e (Euler's number)
- **Secure Evaluation**: Uses AST-based parser (no unsafe eval())
- **Error Handling**: Clear error messages for invalid expressions
- **Keyboard Support**: Type expressions directly

## Usage

```bash
python Calculator.py
```

### Examples

- Basic: `5 + 3 * 2` = 11
- Power: `2^8` = 256
- Trigonometry: `sin(90)` 
- Square root: `√16` = 4
- Constants: `π * 2` ≈ 6.28

## Keyboard Shortcuts

- **Numbers & Operators**: Type directly
- **Enter**: Calculate result
- **C**: Clear display

## Security

This calculator uses Abstract Syntax Tree (AST) parsing instead of Python's `eval()` function, preventing arbitrary code execution while maintaining full mathematical functionality.

## Requirements

- Python 3.6+
- tkinter (built-in)
