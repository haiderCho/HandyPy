import secrets
import string
import pyperclip
import tkinter as tk
from tkinter import ttk


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("430x220")

        # Dark theme
        self.apply_dark_mode()

        # Variables
        self.strength_var = tk.StringVar(value="medium")
        self.length_var = tk.IntVar(value=12)
        self.show_password_var = tk.BooleanVar(value=False)

        self.build_ui()

    # ----------------------------
    # DARK MODE SETUP
    # ----------------------------
    def apply_dark_mode(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            ".",
            background="#1e1e1e",
            foreground="white",
            fieldbackground="#2d2d2d"
        )
        style.configure("TEntry", foreground="white")
        style.map("TCombobox", fieldbackground=[("readonly", "#2d2d2d")])
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#333333",
            bordercolor="#333333",
            background="#4caf50",
            lightcolor="#4caf50",
            darkcolor="#4caf50",
        )

        self.root.configure(bg="#1e1e1e")

    # ----------------------------
    # BUILD UI
    # ----------------------------
    def build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        # Password Length
        ttk.Label(main, text="Length:").grid(row=0, column=0, sticky="w")
        self.length_select = ttk.Combobox(
            main,
            textvariable=self.length_var,
            values=list(range(8, 33)),
            width=5,
            state="readonly",
        )
        self.length_select.grid(row=0, column=1, sticky="w")
        self.length_select.current(0)

        # Strength radio buttons
        ttk.Label(main, text="Strength:").grid(row=1, column=0, sticky="w")

        strengths = [("Low", "low"), ("Medium", "medium"), ("Strong", "strong")]
        for i, (label, value) in enumerate(strengths, start=1):
            ttk.Radiobutton(main, text=label, variable=self.strength_var, value=value).grid(
                row=1, column=i, padx=4, sticky="w"
            )

        # Password output field
        ttk.Label(main, text="Generated Password:").grid(row=2, column=0, pady=(10, 0))

        entry_frame = ttk.Frame(main)
        entry_frame.grid(row=2, column=1, columnspan=3, pady=(10, 0), sticky="w")

        self.output_entry = ttk.Entry(entry_frame, width=35, show="*")
        self.output_entry.grid(row=0, column=0, sticky="w")

        show_btn = ttk.Checkbutton(
            entry_frame,
            text="Show",
            variable=self.show_password_var,
            command=self.toggle_show_password,
        )
        show_btn.grid(row=0, column=1, padx=6)

        # Strength Bar
        ttk.Label(main, text="Password Strength:").grid(
            row=3, column=0, pady=(10, 0), sticky="w"
        )

        self.pw_strength_bar = ttk.Progressbar(
            main, orient="horizontal", length=200, mode="determinate"
        )
        self.pw_strength_bar.grid(
            row=3, column=1, columnspan=3, pady=(10, 0), sticky="w"
        )

        # Buttons
        ttk.Button(main, text="Generate", command=self.generate_password).grid(
            row=0, column=3, padx=(15, 0)
        )
        ttk.Button(main, text="Copy", command=self.copy_to_clipboard).grid(
            row=0, column=4, padx=5
        )

        # Update strength live
        self.output_entry.bind("<KeyRelease>", self.update_strength_bar)

    # ----------------------------
    # GENERATE PASSWORD
    # ----------------------------
    def generate_password(self):
        length = self.length_var.get()
        strength = self.strength_var.get()

        chars = string.ascii_lowercase
        if strength == "medium":
            chars = string.ascii_letters
        elif strength == "strong":
            chars = string.ascii_letters + string.digits + string.punctuation

        password = "".join(secrets.choice(chars) for _ in range(length))

        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, password)
        self.update_strength_bar()

    # ----------------------------
    # COPY PASSWORD
    # ----------------------------
    def copy_to_clipboard(self):
        text = self.output_entry.get()
        if text:
            pyperclip.copy(text)

    # ----------------------------
    # SHOW / HIDE PASSWORD
    # ----------------------------
    def toggle_show_password(self):
        self.output_entry.config(show="" if self.show_password_var.get() else "*")

    # ----------------------------
    # PASSWORD STRENGTH LOGIC
    # ----------------------------
    def update_strength_bar(self, event=None):
        password = self.output_entry.get()
        score = 0

        if len(password) >= 8:
            score += 25
        if any(c.islower() for c in password):
            score += 25
        if any(c.isupper() for c in password):
            score += 25
        if any(c.isdigit() for c in password) or any(not c.isalnum() for c in password):
            score += 25

        self.pw_strength_bar["value"] = score


# Run
if __name__ == "__main__":
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()
