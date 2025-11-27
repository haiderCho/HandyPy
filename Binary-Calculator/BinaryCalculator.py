import tkinter as tk
from tkinter import ttk


# --------------------------- Core Conversion Logic ---------------------------

def binary_to_decimal(n: str) -> int:
    return int(n, 2)


def decimal_to_binary(n: int) -> str:
    return bin(n)[2:] if n >= 0 else "-" + bin(abs(n))[2:]


def add(a, b):
    return decimal_to_binary(binary_to_decimal(a) + binary_to_decimal(b))


def sub(a, b):
    return decimal_to_binary(binary_to_decimal(a) - binary_to_decimal(b))


def mul(a, b):
    return decimal_to_binary(binary_to_decimal(a) * binary_to_decimal(b))


def div(a, b):
    b_val = binary_to_decimal(b)
    if b_val == 0:
        return "Err"
    result = binary_to_decimal(a) // b_val
    return decimal_to_binary(result)


# --------------------------- Expression Evaluation ---------------------------

def evaluate_expression(expr: str) -> str:
    for op in "+-X/":
        if op in expr:
            left, right = expr.split(op)
            if not left or not right:
                return ""

            if op == "+":  return add(left, right)
            if op == "-":  return sub(left, right)
            if op == "X":  return mul(left, right)
            if op == "/":  return div(left, right)

    return ""


# --------------------------- UI Handlers ---------------------------

def insert_value(val):
    entry.insert(tk.END, val)


def clear_entry():
    entry.delete(0, tk.END)


def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])


def negate():
    current = entry.get()
    if current.startswith("-"):
        entry.delete(0, tk.END)
        entry.insert(0, current[1:])
    else:
        entry.insert(0, "-")


def convert_bin_to_dec():
    try:
        dec = binary_to_decimal(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(dec))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Err")


def convert_dec_to_bin():
    try:
        val = int(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, decimal_to_binary(val))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Err")


def calculate():
    expr = entry.get()
    result = evaluate_expression(expr)
    entry.delete(0, tk.END)
    entry.insert(0, result)


# --------------------------- UI Setup ---------------------------

window = tk.Tk()
window.title("Standard Binary Calculator")
window.resizable(False, False)

style = ttk.Style()
style.configure("TButton", padding=6, font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 12))

entry = ttk.Entry(window, width=45)
entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

# Button layout matrix
buttons = [
    [("1", lambda: insert_value("1")), ("0", lambda: insert_value("0")),
     ("C", clear_entry), ("=", calculate)],
    [("+", lambda: insert_value("+")), ("-", lambda: insert_value("-")),
     ("X", lambda: insert_value("X")), ("/", lambda: insert_value("/"))],
    [("+/-", negate), ("⌫", backspace),
     ("Bin→Dec", convert_bin_to_dec), ("Dec→Bin", convert_dec_to_bin)],
]

for r, row in enumerate(buttons, start=1):
    for c, (text, cmd) in enumerate(row):
        ttk.Button(window, text=text, command=cmd).grid(
            row=r, column=c, padx=5, pady=5, ipadx=5
        )

window.mainloop()