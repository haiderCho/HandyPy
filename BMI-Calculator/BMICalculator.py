import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class BMICalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BMI Calculator")
        self.resizable(False, False)

        self.weight_var = tk.StringVar()
        self.feet_var = tk.StringVar()
        self.inch_var = tk.StringVar()

        self.configure_style()
        self.build_ui()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Unified color scheme
        bg = "#F2F2F2"
        fg = "#000000"
        accent = "#D0D0D0"

        style.configure(".", background=bg, foreground=fg)
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 14))
        style.configure("Header.TLabel", font=("Segoe UI", 28, "bold"))
        style.configure("TEntry", fieldbackground="#FFFFFF")
        style.configure("TButton", font=("Segoe UI", 14, "bold"), background=accent)

        self.config(background=bg)

    def build_ui(self):
        header = ttk.Label(self, text="Body Mass Index", style="Header.TLabel")
        header.grid(row=0, column=0, pady=15)

        main = ttk.Frame(self)
        main.grid(row=1, column=0, padx=20, pady=10)

        # Weight
        ttk.Label(main, text="Weight (kg):").grid(row=0, column=0, sticky="w")
        ttk.Entry(main, textvariable=self.weight_var, width=25).grid(
            row=1, column=0, pady=5, sticky="w"
        )

        # Height
        ttk.Label(main, text="Height:").grid(row=2, column=0, pady=(20, 0), sticky="w")

        height_frame = ttk.Frame(main)
        height_frame.grid(row=3, column=0, pady=5, sticky="w")

        ttk.Label(height_frame, text="Feet:").grid(row=0, column=0, sticky="w")
        ttk.Entry(height_frame, textvariable=self.feet_var, width=8).grid(
            row=0, column=1, padx=(5, 20)
        )

        ttk.Label(height_frame, text="Inches:").grid(row=0, column=2, sticky="w")
        ttk.Entry(height_frame, textvariable=self.inch_var, width=8).grid(
            row=0, column=3, padx=5
        )

        # Results
        self.result_label = ttk.Label(main, text="", font=("Segoe UI", 20, "bold"))
        self.result_label.grid(row=4, column=0, pady=(25, 5))

        self.category_label = ttk.Label(main, text="", font=("Segoe UI", 14))
        self.category_label.grid(row=5, column=0)

        # Button
        ttk.Button(main, text="Calculate BMI", command=self.calculate_bmi).grid(
            row=6, column=0, pady=25
        )

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            feet = float(self.feet_var.get())
            inches = float(self.inch_var.get())

            if weight <= 0 or feet < 0 or inches < 0:
                raise ValueError

            total_inches = feet * 12 + inches
            height_m = total_inches * 0.0254

            if height_m <= 0:
                raise ValueError

            bmi = round(weight / (height_m ** 2), 2)

            self.result_label.config(text=f"BMI: {bmi}")
            self.category_label.config(text=self.classify_bmi(bmi))

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid weight and height values.")

    @staticmethod
    def classify_bmi(bmi):
        if bmi < 18.5:
            return "Classification: Underweight"
        elif 18.5 <= bmi < 25:
            return "Classification: Normal weight"
        elif 25 <= bmi < 30:
            return "Classification: Overweight"
        elif 30 <= bmi < 35:
            return "Classification: Obesity Class I"
        elif 35 <= bmi < 40:
            return "Classification: Obesity Class II"
        else:
            return "Classification: Obesity Class III"


if __name__ == "__main__":
    app = BMICalculator()
    app.mainloop()
