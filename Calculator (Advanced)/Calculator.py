import tkinter as tk
from math import sin, cos, tan, log, sqrt, pi, e

# ------------------ Setup ------------------
root = tk.Tk()
root.title("Advanced Calculator")
root.resizable(0, 0)

# ------------------ Global Variables ------------------
current_expression = ""

# ------------------ Functions ------------------
def update_display(expr):
    display_var.set(expr)

def button_click(value):
    global current_expression
    current_expression += str(value)
    update_display(current_expression)

def button_clear():
    global current_expression
    current_expression = ""
    update_display(current_expression)

def button_equal():
    global current_expression
    try:
        result = eval_expression(current_expression)
        current_expression = str(result)
    except Exception:
        current_expression = "Error"
    update_display(current_expression)

def eval_expression(expr):
    expr = expr.replace("√", "sqrt")
    expr = expr.replace("^", "**")
    expr = expr.replace("π", str(pi))
    expr = expr.replace("e", str(e))
    return eval(expr, {"sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e})

def key_press(event):
    key = event.char
    if key.isdigit() or key in ".+-*/^":
        button_click(key)
    elif key == "\r":
        button_equal()
    elif key.lower() == "c":
        button_clear()

# ------------------ Display ------------------
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Calibri", 20),
                   bd=5, relief=tk.RIDGE, justify='right')
display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="we")

# ------------------ Button Definitions ------------------
buttons = {}
btn_texts = [
    ['7','8','9','/','AC'],
    ['4','5','6','*','^'],
    ['1','2','3','-','√'],
    ['0','.','=','+','log'],
    ['π','e','sin','cos','tan']
]

btn_frame = tk.Frame(root)
btn_frame.grid(row=1, column=0, columnspan=6)

for r, row in enumerate(btn_texts):
    for c, text in enumerate(row):
        command = lambda t=text: button_click(t)
        if text == "AC":
            command = button_clear
        elif text == "=":
            command = button_equal
        btn = tk.Button(btn_frame, text=text, width=5, height=2, font=("Calibri", 12),
                        command=command)
        btn.grid(row=r, column=c, padx=2, pady=2)
        buttons[text] = btn

# ------------------ Keyboard Bindings ------------------
root.bind("<Key>", key_press)

# ------------------ Run ------------------
root.mainloop()
