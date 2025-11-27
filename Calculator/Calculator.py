import tkinter as tk
from math import sin, cos, tan, log, sqrt, pi, e
import ast
import operator
import re

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
    except ValueError as ve:
        current_expression = "Math Error"
    except ZeroDivisionError:
        current_expression = "Div by 0"
    except Exception as e:
        current_expression = "Error"
    update_display(current_expression)

def safe_eval(expr):
    """
    Safely evaluate mathematical expressions without using eval().
    Supports basic arithmetic, power, and mathematical functions.
    """
    # Replace special symbols
    expr = expr.replace("√", "sqrt")
    expr = expr.replace("^", "**")
    expr = expr.replace("π", str(pi))
    
    # Handle 'e' carefully - replace standalone 'e' with Euler's number
    # but don't replace 'e' that's part of function names
    expr = re.sub(r'\be\b', str(e), expr)
    
    # Whitelist of allowed operations and functions
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    allowed_functions = {
        'sin': sin,
        'cos': cos,
        'tan': tan,
        'log': log,
        'sqrt': sqrt,
    }
    
    def eval_node(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = eval_node(node.left)
            right = eval_node(node.right)
            op = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Operator {type(node.op).__name__} not allowed")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
            operand = eval_node(node.operand)
            op = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Operator {type(node.op).__name__} not allowed")
            return op(operand)
        elif isinstance(node, ast.Call):  # function call
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls allowed")
            func_name = node.func.id
            func = allowed_functions.get(func_name)
            if func is None:
                raise ValueError(f"Function {func_name} not allowed")
            args = [eval_node(arg) for arg in node.args]
            return func(*args)
        else:
            raise ValueError(f"Node type {type(node).__name__} not allowed")
    
    try:
        tree = ast.parse(expr, mode='eval')
        return eval_node(tree.body)
    except (SyntaxError, ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def eval_expression(expr):
    """Wrapper for backward compatibility"""
    return safe_eval(expr)

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
