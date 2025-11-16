# tkinter and time modules are inbuilt
import time
import tkinter as tk
from tkinter import ttk


class StopwatchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stopwatch")
        self.configure(bg="#1e1e1e")  # Dark mode

        # Window center positioning
        width, height = 420, 180
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = int((screen_w - width) / 2)
        y = int((screen_h - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        self.stopwatch = StopWatch(self)
        self.stopwatch.pack(pady=15)

        self._create_buttons()

    def _create_buttons(self):
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.pack(pady=10)

        self.start_btn = tk.Button(
            frame, text="Start", width=12, height=2,
            bg="#2ecc71", fg="white", bd=0, activebackground="#27ae60",
            command=self._toggle_start
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(
            frame, text="Stop", width=12, height=2,
            bg="#e74c3c", fg="white", bd=0, activebackground="#c0392b",
            command=self.stopwatch.stop
        )
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(
            frame, text="Reset", width=12, height=2,
            bg="#34495e", fg="white", bd=0, activebackground="#2c3e50",
            command=self.stopwatch.reset
        )
        self.reset_btn.grid(row=0, column=2, padx=5)

    def _toggle_start(self):
        if not self.stopwatch.running:
            self.stopwatch.start()
            self.start_btn.config(text="Running...", bg="#16a085")
        else:
            self.stopwatch.stop()
            self.start_btn.config(text="Start", bg="#2ecc71")


class StopWatch(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")

        self.start_time = 0.0
        self.elapsed = 0.0
        self.running = False
        self.timer = None

        self.time_var = tk.StringVar(value="00:00:00")

        self.label = tk.Label(
            self, textvariable=self.time_var,
            font=("Consolas", 48, "bold"),
            fg="#f1c40f", bg="#1e1e1e"
        )
        self.label.pack()

    # --- Time formatting ---
    @staticmethod
    def _format_time(elapsed):
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        ms = int((elapsed - int(elapsed)) * 100)
        return f"{mins:02d}:{secs:02d}:{ms:02d}"

    # --- Stopwatch Controls ---
    def _update(self):
        self.elapsed = time.time() - self.start_time
        self.time_var.set(self._format_time(self.elapsed))
        self.timer = self.after(10, self._update)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True
            self._update()

    def stop(self):
        if self.running:
            self.after_cancel(self.timer)
            self.running = False

    def reset(self):
        self.stop()
        self.elapsed = 0.0
        self.time_var.set("00:00:00")


if __name__ == "__main__":
    StopwatchApp().mainloop()
