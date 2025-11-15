import json
import math
import tkinter as tk
from tkinter import ttk, messagebox
from urllib import request, error
from functools import partial
from typing import Dict, Optional

# ---------------------------
# Utilities
# ---------------------------
def fetch_json(url: str, timeout: float = 6.0) -> Optional[dict]:
    """Fetch JSON from a URL. Return None on failure."""
    try:
        with request.urlopen(url, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except Exception:
        return None

# ---------------------------
# App class
# ---------------------------
class ConverterApp(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.title("All-in-One Converter")
        self.master.geometry("620x420")
        self.master.minsize(540, 380)
        self.style = ttk.Style(self.master)

        # Palettes
        self.light_palette = {
            "bg": "#f6f7fb",
            "card": "#ffffff",
            "fg": "#222222",
            "accent": "#007acc",
            "muted": "#6b7280",
            "entry_bg": "#ffffff",
        }
        self.dark_palette = {
            "bg": "#0f1724",
            "card": "#111827",
            "fg": "#e6eef6",
            "accent": "#48b0ff",
            "muted": "#94a3b8",
            "entry_bg": "#0b1220",
        }
        self.current_palette = self.light_palette

        # Currency rates cache: base -> {rates..., date:...}
        self.rates_cache: Dict[str, dict] = {}

        self._configure_styles()
        self._build_ui()

    # ---------------------------
    # Styling
    # ---------------------------
    def _configure_styles(self):
        # Base theme
        self.style.theme_use("clam")

        # Generic ttk styles
        self.style.configure("Header.TLabel", font=("Inter", 16, "bold"))
        self.style.configure("SubHeader.TLabel", font=("Inter", 11))
        self.style.configure("Card.TFrame", relief="flat", borderwidth=0, padding=12)
        self.style.configure("Accent.TButton", font=("Inter", 10, "bold"), relief="flat")
        self.style.map("Accent.TButton",
                       background=[("active", "!disabled", self.current_palette["accent"])],
                       foreground=[("!disabled", self.current_palette["card"])])

        # Entry style adjustments (ttk.Entry uses 'TEntry')
        self.style.configure("TEntry", padding=6)

        self._apply_palette(self.light_palette)

    def _apply_palette(self, palette: dict):
        self.current_palette = palette
        bg = palette["bg"]
        card = palette["card"]
        fg = palette["fg"]
        muted = palette["muted"]
        accent = palette["accent"]

        # Root bg
        self.master.configure(bg=bg)
        self.configure(style="Card.TFrame")
        self.style.configure(".", background=bg, foreground=fg)
        self.style.configure("Card.TFrame", background=card)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", background=card, foreground=fg)
        self.style.configure("Accent.TButton", background=accent, foreground=card)
        self.style.configure("TNotebook", background=bg)
        self.style.configure("TNotebook.Tab", padding=(10, 6))
        self.style.map("TNotebook.Tab",
                       background=[("selected", card)],
                       foreground=[("selected", fg)])

        # Set widget-specific colors via element options where needed (Entries, Combobox)
        self.style.configure("TEntry", fieldbackground=palette["entry_bg"], background=palette["entry_bg"], foreground=fg)
        self.style.configure("TCombobox", fieldbackground=palette["entry_bg"], background=palette["entry_bg"], foreground=fg)

    def toggle_theme(self):
        if self.current_palette is self.light_palette:
            self._apply_palette(self.dark_palette)
        else:
            self._apply_palette(self.light_palette)

    # ---------------------------
    # UI Build
    # ---------------------------
    def _build_ui(self):
        # Top frame with title + controls
        top = ttk.Frame(self, style="Card.TFrame")
        top.pack(side="top", fill="x", padx=14, pady=(12, 6))

        title = ttk.Label(top, text="ALL-IN-ONE CONVERTER", style="Header.TLabel")
        title.grid(row=0, column=0, sticky="w")

        # Theme toggle + Quit
        controls = ttk.Frame(top, style="Card.TFrame")
        controls.grid(row=0, column=1, sticky="e")
        theme_btn = ttk.Button(controls, text="Toggle Theme", style="Accent.TButton", command=self.toggle_theme)
        theme_btn.pack(side="right", padx=(6, 0))
        quit_btn = ttk.Button(controls, text="Quit", command=self.master.destroy)
        quit_btn.pack(side="right", padx=6)

        # Notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=14, pady=6)

        # Tabs
        notebook.add(self._currency_tab(), text="Currency")
        notebook.add(self._weight_tab(), text="Weight")
        notebook.add(self._length_tab(), text="Length")
        notebook.add(self._area_tab(), text="Area")
        notebook.add(self._temperature_tab(), text="Temperature")

        self.pack(fill="both", expand=True)

    # ---------------------------
    # Currency Tab
    # ---------------------------
    def _currency_tab(self):
        frame = ttk.Frame(self, style="Card.TFrame")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        ttk.Label(frame, text="Currency Converter", style="SubHeader.TLabel").grid(column=0, row=0, columnspan=3, sticky="w", pady=(0, 8))

        CURRENCIES = ["USD", "EUR", "INR", "GBP", "JPY", "CNY", "AED", "QAR", "ZWD"]

        # Input
        amount_var = tk.StringVar(value="1")
        from_var = tk.StringVar(value="USD")
        to_var = tk.StringVar(value="EUR")
        result_var = tk.StringVar(value="")

        ttk.Label(frame, text="Amount:").grid(column=0, row=1, sticky="w")
        amount_entry = ttk.Entry(frame, textvariable=amount_var)
        amount_entry.grid(column=1, row=1, sticky="ew", padx=6)

        ttk.Label(frame, text="From:").grid(column=0, row=2, sticky="w", pady=(6,0))
        from_box = ttk.Combobox(frame, values=CURRENCIES, textvariable=from_var, state="readonly")
        from_box.grid(column=1, row=2, sticky="ew", padx=6, pady=(6,0))

        ttk.Label(frame, text="To:").grid(column=0, row=3, sticky="w", pady=(6,0))
        to_box = ttk.Combobox(frame, values=CURRENCIES, textvariable=to_var, state="readonly")
        to_box.grid(column=1, row=3, sticky="ew", padx=6, pady=(6,0))

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(column=0, row=4, columnspan=3, pady=(10, 6), sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        convert_btn = ttk.Button(btn_frame, text="Convert", style="Accent.TButton",
                                 command=lambda: self._do_currency_convert(amount_var, from_var, to_var, result_var))
        convert_btn.grid(column=0, row=0, padx=6, sticky="ew")
        refresh_btn = ttk.Button(btn_frame, text="Refresh Rates",
                                 command=lambda: self._refresh_rates(from_var.get()))
        refresh_btn.grid(column=1, row=0, padx=6, sticky="ew")

        ttk.Label(frame, text="Result:", anchor="w").grid(column=0, row=5, sticky="w")
        result_entry = ttk.Entry(frame, textvariable=result_var, state="readonly")
        result_entry.grid(column=1, row=5, sticky="ew", padx=6, pady=(6,0))

        # Small note
        note = ttk.Label(frame, text="Rates fetched from exchangerate.host (online). Fallback to sample rates if offline.",
                         font=("Inter", 8))
        note.grid(column=0, row=6, columnspan=3, sticky="w", pady=(8, 0))

        for child in frame.winfo_children():
            child.grid_configure(padx=8, pady=4)

        return frame

    def _refresh_rates(self, base: str):
        """Fetch latest rates for base currency and cache them."""
        url = f"https://api.exchangerate.host/latest?base={base}"
        data = fetch_json(url)
        if data and "rates" in data:
            self.rates_cache[base] = data
            messagebox.showinfo("Rates Refreshed", f"Rates for {base} updated (date: {data.get('date', 'n/a')}).")
        else:
            messagebox.showwarning("Fetch Failed", "Could not fetch live rates. Using cached or fallback rates.")

    def _do_currency_convert(self, amount_var, from_var, to_var, result_var):
        amt_text = amount_var.get().strip()
        try:
            amt = float(amt_text)
        except ValueError:
            result_var.set("Invalid amount")
            return

        frm = from_var.get()
        to = to_var.get()
        if not frm or not to:
            result_var.set("Select currencies")
            return
        # Try to get rates from cache or fetch once
        data = self.rates_cache.get(frm)
        if not data:
            data = fetch_json(f"https://api.exchangerate.host/latest?base={frm}")
            if data and "rates" in data:
                self.rates_cache[frm] = data

        if data and "rates" in data and to in data["rates"]:
            rate = data["rates"][to]
            converted = amt * rate
            result_var.set(f"{converted:.6g} {to}")
            return

        # Fallback: use a small built-in sample table (rates approximate, for offline mode)
        fallback_rates = {
            "USD": {"EUR": 0.91, "INR": 83.5, "GBP": 0.78, "JPY": 154.0, "CNY": 7.3, "AED": 3.67, "QAR": 3.64, "ZWD": 322.0},
            "EUR": {"USD": 1.09, "INR": 91.5, "GBP": 0.85},
            "INR": {"USD": 0.012, "EUR": 0.011},
        }
        rate = fallback_rates.get(frm, {}).get(to)
        if rate:
            result_var.set(f"{amt * rate:.6g} {to} (fallback)")
        else:
            result_var.set("Rate not available")

    # ---------------------------
    # Weight Tab
    # ---------------------------
    def _weight_tab(self):
        frame = ttk.Frame(self, style="Card.TFrame")
        ttk.Label(frame, text="Weight Converter (metric unit prefixes)", style="SubHeader.TLabel").grid(column=0, row=0, columnspan=3, sticky="w")

        units = {
            "tonne": 1_000_000.0,  # grams
            "kg": 1000.0,
            "hg": 100.0,
            "dag": 10.0,
            "g": 1.0,
            "dg": 0.1,
            "cg": 0.01,
            "mg": 0.001,
        }

        in_var = tk.StringVar(value="g")
        out_var = tk.StringVar(value="kg")
        amt_var = tk.StringVar(value="1000")
        result_var = tk.StringVar()

        ttk.Label(frame, text="Value:").grid(column=0, row=1, sticky="w")
        ttk.Entry(frame, textvariable=amt_var).grid(column=1, row=1, sticky="ew")

        ttk.Label(frame, text="From:").grid(column=0, row=2, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=in_var, state="readonly").grid(column=1, row=2, sticky="ew")

        ttk.Label(frame, text="To:").grid(column=0, row=3, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=out_var, state="readonly").grid(column=1, row=3, sticky="ew")

        conv_btn = ttk.Button(frame, text="Convert", style="Accent.TButton",
                              command=lambda: self._generic_factor_convert(amt_var, in_var, out_var, result_var, units))
        conv_btn.grid(column=0, row=4, columnspan=2, sticky="ew", pady=8)

        ttk.Label(frame, text="Result:").grid(column=0, row=5, sticky="w")
        ttk.Entry(frame, textvariable=result_var, state="readonly").grid(column=1, row=5, sticky="ew")

        for child in frame.winfo_children():
            child.grid_configure(padx=8, pady=6)

        return frame

    # ---------------------------
    # Length Tab
    # ---------------------------
    def _length_tab(self):
        frame = ttk.Frame(self, style="Card.TFrame")
        ttk.Label(frame, text="Length Converter", style="SubHeader.TLabel").grid(column=0, row=0, columnspan=3, sticky="w")

        units = {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1.0,
            "km": 1000.0,
            "inch": 0.0254,
            "ft": 0.3048,
            "yd": 0.9144,
            "mi": 1609.34,
            "nmi": 1852.0,
        }

        in_var = tk.StringVar(value="m")
        out_var = tk.StringVar(value="km")
        amt_var = tk.StringVar(value="1500")
        result_var = tk.StringVar()

        ttk.Label(frame, text="Value:").grid(column=0, row=1, sticky="w")
        ttk.Entry(frame, textvariable=amt_var).grid(column=1, row=1, sticky="ew")

        ttk.Label(frame, text="From:").grid(column=0, row=2, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=in_var, state="readonly").grid(column=1, row=2, sticky="ew")

        ttk.Label(frame, text="To:").grid(column=0, row=3, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=out_var, state="readonly").grid(column=1, row=3, sticky="ew")

        conv_btn = ttk.Button(frame, text="Convert", style="Accent.TButton",
                              command=lambda: self._generic_factor_convert(amt_var, in_var, out_var, result_var, units))
        conv_btn.grid(column=0, row=4, columnspan=2, sticky="ew", pady=8)

        ttk.Label(frame, text="Result:").grid(column=0, row=5, sticky="w")
        ttk.Entry(frame, textvariable=result_var, state="readonly").grid(column=1, row=5, sticky="ew")

        for child in frame.winfo_children():
            child.grid_configure(padx=8, pady=6)

        return frame

    # ---------------------------
    # Area Tab
    # ---------------------------
    def _area_tab(self):
        frame = ttk.Frame(self, style="Card.TFrame")
        ttk.Label(frame, text="Area Converter", style="SubHeader.TLabel").grid(column=0, row=0, columnspan=3, sticky="w")

        units = {
            "square mm": 1e-6,
            "square cm": 1e-4,
            "square m": 1.0,
            "square km": 1e6,
            "square inch": 0.00064516,
            "square foot": 0.09290304,
            "square yard": 0.83612736,
            "acre": 4046.8564224,
            "hectare": 10000.0,
            "square mile": 2589988.110336,
        }

        in_var = tk.StringVar(value="square m")
        out_var = tk.StringVar(value="square km")
        amt_var = tk.StringVar(value="10000")
        result_var = tk.StringVar()

        ttk.Label(frame, text="Value:").grid(column=0, row=1, sticky="w")
        ttk.Entry(frame, textvariable=amt_var).grid(column=1, row=1, sticky="ew")

        ttk.Label(frame, text="From:").grid(column=0, row=2, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=in_var, state="readonly", width=20).grid(column=1, row=2, sticky="ew")

        ttk.Label(frame, text="To:").grid(column=0, row=3, sticky="w")
        ttk.Combobox(frame, values=list(units.keys()), textvariable=out_var, state="readonly", width=20).grid(column=1, row=3, sticky="ew")

        conv_btn = ttk.Button(frame, text="Convert", style="Accent.TButton",
                              command=lambda: self._generic_factor_convert(amt_var, in_var, out_var, result_var, units))
        conv_btn.grid(column=0, row=4, columnspan=2, sticky="ew", pady=8)

        ttk.Label(frame, text="Result:").grid(column=0, row=5, sticky="w")
        ttk.Entry(frame, textvariable=result_var, state="readonly").grid(column=1, row=5, sticky="ew")

        for child in frame.winfo_children():
            child.grid_configure(padx=8, pady=6)

        return frame

    # ---------------------------
    # Temperature Tab
    # ---------------------------
    def _temperature_tab(self):
        frame = ttk.Frame(self, style="Card.TFrame")
        ttk.Label(frame, text="Temperature Converter", style="SubHeader.TLabel").grid(column=0, row=0, columnspan=3, sticky="w")

        # We support Celsius, Fahrenheit, Kelvin
        amt_var = tk.StringVar(value="0")
        in_var = tk.StringVar(value="C")
        out_var = tk.StringVar(value="F")
        result_var = tk.StringVar()

        ttk.Label(frame, text="Value:").grid(column=0, row=1, sticky="w")
        ttk.Entry(frame, textvariable=amt_var).grid(column=1, row=1, sticky="ew")

        ttk.Label(frame, text="From:").grid(column=0, row=2, sticky="w")
        ttk.Combobox(frame, values=["C", "F", "K"], textvariable=in_var, state="readonly").grid(column=1, row=2, sticky="ew")

        ttk.Label(frame, text="To:").grid(column=0, row=3, sticky="w")
        ttk.Combobox(frame, values=["C", "F", "K"], textvariable=out_var, state="readonly").grid(column=1, row=3, sticky="ew")

        conv_btn = ttk.Button(frame, text="Convert", style="Accent.TButton",
                              command=lambda: self._convert_temperature(amt_var, in_var, out_var, result_var))
        conv_btn.grid(column=0, row=4, columnspan=2, sticky="ew", pady=8)

        ttk.Label(frame, text="Result:").grid(column=0, row=5, sticky="w")
        ttk.Entry(frame, textvariable=result_var, state="readonly").grid(column=1, row=5, sticky="ew")

        for child in frame.winfo_children():
            child.grid_configure(padx=8, pady=6)

        return frame

    # ---------------------------
    # Generic factor-based converter
    # ---------------------------
    def _generic_factor_convert(self, amt_var, in_var, out_var, result_var, factors: dict):
        amt_text = amt_var.get().strip()
        try:
            amt = float(amt_text)
        except ValueError:
            result_var.set("Invalid input")
            return
        frm = in_var.get()
        to = out_var.get()
        if frm not in factors or to not in factors:
            result_var.set("Select valid units")
            return
        # Convert via base unit (value * factor[from] grams/meters etc -> /factor[to])
        base_value = amt * factors[frm]
        converted = base_value / factors[to]
        # Pretty formatting: avoid scientific for reasonable numbers
        if abs(converted) >= 1e6 or (0 < abs(converted) < 1e-4):
            formatted = f"{converted:.6e}"
        else:
            formatted = f"{converted:.6g}"
        result_var.set(formatted)

    # ---------------------------
    # Temperature converter
    # ---------------------------
    def _convert_temperature(self, amt_var, in_var, out_var, result_var):
        t_text = amt_var.get().strip()
        try:
            t = float(t_text)
        except ValueError:
            result_var.set("Invalid input")
            return
        frm = in_var.get()
        to = out_var.get()
        # Convert to Celsius first
        if frm == "C":
            c = t
        elif frm == "F":
            c = (t - 32.0) * 5.0 / 9.0
        elif frm == "K":
            c = t - 273.15
        else:
            result_var.set("Unknown unit")
            return

        if to == "C":
            out = c
        elif to == "F":
            out = c * 9.0 / 5.0 + 32.0
        elif to == "K":
            out = c + 273.15
        else:
            result_var.set("Unknown unit")
            return

        # formatting
        if abs(out) < 1e-3 or abs(out) >= 1e6:
            result_var.set(f"{out:.6e}")
        else:
            # Show up to 4 decimals sensibly
            if math.isclose(out, round(out, 2)):
                result_var.set(f"{out:.2f}")
            else:
                result_var.set(f"{out:.4g}")

# ---------------------------
# Run the app
# ---------------------------
def main():
    root = tk.Tk()
    # Set some default font family if available
    try:
        root.option_add("*Font", "Inter 10")
    except Exception:
        pass
    app = ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
