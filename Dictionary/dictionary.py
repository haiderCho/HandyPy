import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"


class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        header = tk.Label(
            self.root,
            text="DICTIONARY",
            font=("Helvetica", 32, "bold"),
            fg="#1a73e8"
        )
        header.pack(pady=15)

        # Input frame
        input_frame = tk.Frame(self.root)
        tk.Label(input_frame, text="Enter Word:", font=("Helvetica", 14)).pack(side=tk.LEFT)
        self.word_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=22)
        self.word_entry.pack(side=tk.LEFT, padx=10)
        input_frame.pack(pady=10)

        # Search button
        search_btn = tk.Button(
            self.root,
            text="Search",
            font=("Helvetica", 14, "bold"),
            bg="#1a73e8",
            fg="white",
            relief=tk.FLAT,
            command=self.get_meaning
        )
        search_btn.pack(pady=10)

        # Meaning display
        meaning_frame = tk.Frame(self.root)
        tk.Label(meaning_frame, text="Meaning:", font=("Helvetica", 14, "bold")).pack(anchor="w")
        self.meaning_label = tk.Label(
            meaning_frame,
            text="",
            font=("Helvetica", 12),
            wraplength=450,
            justify="left"
        )
        self.meaning_label.pack(anchor="w", pady=5)
        meaning_frame.pack(pady=10)

    def get_meaning(self):
        word = self.word_entry.get().strip()
        if not word:
            messagebox.showwarning("Error", "Enter a word.")
            return

        try:
            response = requests.get(API_URL.format(word))
            data = response.json()

            if isinstance(data, dict) and "title" in data:
                self.meaning_label.config(text="Invalid or unknown word.")
                return

            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            self.meaning_label.config(text=meaning)

        except Exception:
            messagebox.showerror("Error", "Unable to fetch meaning at this time.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
