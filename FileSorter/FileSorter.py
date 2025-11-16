import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


class FileSorter:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern File Sorter")
        self.root.geometry("420x260")
        self.root.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Modern dark theme styling
        self.style.configure(
            "TButton",
            padding=8,
            relief="flat",
            background="#444",
            foreground="white",
            font=("Segoe UI", 10)
        )
        self.style.map("TButton",
                       background=[("active", "#666")])

        self.style.configure(
            "TLabel",
            background="#1e1e1e",
            foreground="white",
            font=("Segoe UI", 10)
        )

        ttk.Label(root, text="Modern File Sorter", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.select_button = ttk.Button(
            root, text="Select Directory", command=self.select_directory
        )
        self.select_button.pack(pady=5)

        self.sort_button = ttk.Button(
            root, text="Sort Files", command=self.sort_files
        )
        self.sort_button.pack(pady=5)

        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=15)

        self.dir_path = None

    def select_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            self.status_label.config(text=f"Selected: {dir_path}")
        else:
            self.status_label.config(text="No directory selected.")

    def sort_files(self):
        if not self.dir_path:
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return

        files = [f for f in os.listdir(self.dir_path)
                 if os.path.isfile(os.path.join(self.dir_path, f))]

        if not files:
            self.status_label.config(text="No files found.")
            return

        sorted_count = 0

        for filename in files:
            if "." not in filename:
                continue

            ext = filename.split(".")[-1].lower().strip()
            if not ext:
                continue

            target_dir = os.path.join(self.dir_path, ext)

            os.makedirs(target_dir, exist_ok=True)

            source = os.path.join(self.dir_path, filename)
            target = os.path.join(target_dir, filename)

            try:
                shutil.move(source, target)
                sorted_count += 1
            except Exception as e:
                print("Failed:", e)

        self.status_label.config(text=f"Sorted {sorted_count} files successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    FileSorter(root)
    root.mainloop()
