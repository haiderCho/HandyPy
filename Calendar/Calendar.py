# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import calendar


def show_calendar():
    year_text = year_field.get().strip()

    if not year_text.isdigit():
        messagebox.showerror("Invalid Input", "Enter a valid numeric year.")
        return

    year_val = int(year_text)

    top = tk.Toplevel(root)
    top.title(f"Calendar – {year_val}")
    top.geometry("620x650")

    header = ttk.Label(top, text=f"Calendar for {year_val}",
                       font=("Helvetica", 20, "bold"))
    header.pack(pady=10)

    cal_data = calendar.calendar(year_val)
    cal_label = tk.Text(top, font=("Consolas", 11), wrap="none", borderwidth=0)
    cal_label.insert("1.0", cal_data)
    cal_label.config(state="disabled")
    cal_label.pack(expand=True, fill="both", padx=10, pady=10)


root = tk.Tk()
root.title("Calendar Viewer")
root.geometry("320x200")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")

title_label = ttk.Label(main_frame, text="Calendar", font=("Helvetica", 24, "bold"))
title_label.pack(pady=5)

year_label = ttk.Label(main_frame, text="Enter Year:")
year_label.pack(pady=(10, 3))

year_field = ttk.Entry(main_frame, width=20)
year_field.pack()

btn_show = ttk.Button(main_frame, text="Show Calendar", command=show_calendar)
btn_show.pack(pady=15)

btn_close = ttk.Button(main_frame, text="Close", command=root.destroy)
btn_close.pack()

root.mainloop()
