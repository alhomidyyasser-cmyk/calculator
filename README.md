# Professional Calculator

A lightweight desktop calculator built with Python and Tkinter. The interface is in Arabic and supports everyday arithmetic, scientific functions, memory, and a reusable calculation history.

## Features

- Addition, subtraction, multiplication, division, powers, and remainder (`%`)
- Parentheses, decimal numbers, unary plus/minus, and the constants `pi` and `e`
- Scientific functions: `sqrt`, `sin`, `cos`, `tan`, `log` (base 10), `ln` (natural logarithm), and `abs`
- Memory controls: `MC` (clear), `MR` (recall), `M+` (add), and `M−` (subtract)
- Calculation history; double-click an entry to reuse its result
- Keyboard shortcuts: **Enter** calculates and **Esc** clears the current expression
- A restricted expression evaluator that supports only the calculator's documented operations; it does not use Python's `eval`

Trigonometric functions use radians. The `%` key calculates the remainder, rather than a percentage of another value.

## Requirements

- Python 3.9 or later
- Tkinter, which is included with most standard Python distributions. On some Linux distributions it must be installed separately (often provided by the `python3-tk` package).

No third-party Python packages are required.

## Run

From the project directory, start the application with:

```powershell
py main2.py
```

On systems where `python3` is the Python command, use:

```sh
python3 main2.py
```

## Run tests

The test suite uses Python's standard-library `unittest`:

```sh
python -m unittest discover -v
```
