import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class AgeCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Age Calculator")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.mode = tk.StringVar(value="light")
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.update_theme()

    def update_theme(self):
        if self.mode.get() == "light":
            self.bg_color = "#E6F2FF"
            self.fg_color = "#000000"
            self.btn_color = "#007ACC"
        else:
            self.bg_color = "#2E2E2E"
            self.fg_color = "#FFFFFF"
            self.btn_color = "#1E90FF"

        self.root.configure(bg=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10, "bold"))
        self.style.map("TButton",
                       background=[("active", self.btn_color)],
                       foreground=[("active", "#FFFFFF")])

    def create_widgets(self):
        # Theme toggle
        ttk.Label(self.root, text="Theme:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        theme_toggle = ttk.Combobox(self.root, textvariable=self.mode, values=["light", "dark"], state="readonly", width=10)
        theme_toggle.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        theme_toggle.bind("<<ComboboxSelected>>", lambda e: self.update_theme())

        # Input fields
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.add_label_entry("Year:", self.year_var, 1)
        self.add_label_entry("Month:", self.month_var, 2)
        self.add_label_entry("Day:", self.day_var, 3)

        # Calculate button
        calc_button = ttk.Button(self.root, text="Calculate Age", command=self.calculate_age)
        calc_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Result label
        self.result_label = ttk.Label(self.root, text="", font=("Helvetica", 10, "bold"), justify="left")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

    def add_label_entry(self, text, variable, row):
        ttk.Label(self.root, text=text).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=variable).grid(row=row, column=1, padx=10, pady=5, sticky="w")

    def validate_date(self, year, month, day):
        try:
            y, m, d = int(year), int(month), int(day)
            birth_date = date(y, m, d)
            if birth_date > date.today():
                messagebox.showerror("Invalid Date", "Birth date cannot be in the future.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Year, Month, and Day.")
            return False

    def calculate_age(self):
        year, month, day = self.year_var.get(), self.month_var.get(), self.day_var.get()

        if not self.validate_date(year, month, day):
            return

        birth_date = date(int(year), int(month), int(day))
        today = date.today()

        # Exact age calculation in years, months, days
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days_in_prev_month = (date(prev_year, prev_month % 12 + 1, 1) - date(prev_year, prev_month, 1)).days
            days += days_in_prev_month

        if months < 0:
            years -= 1
            months += 12

        # Total calculations
        total_months = years * 12 + months
        total_weeks = (today - birth_date).days // 7
        total_days = (today - birth_date).days
        total_hours = total_days * 24

        result_text = (
            f"Exact Age: {years} years, {months} months, {days} days\n"
            f"Age in Months: {total_months} Months\n"
            f"Age in Weeks: {total_weeks} Weeks\n"
            f"Age in Days: {total_days} Days\n"
            f"Age in Hours: {total_hours} Hours"
        )
        self.result_label.config(text=result_text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AgeCalculator()
    app.run()

