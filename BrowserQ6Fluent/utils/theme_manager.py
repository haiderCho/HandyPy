from qfluentwidgets import setTheme, Theme, setThemeColor
from PyQt6.QtGui import QColor
from config import cfg

class ThemeManager:
    @staticmethod
    def apply_theme():
        # Apply Dark/Light mode
        if cfg.get("dark_mode"):
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.LIGHT)
            
        # Apply accent color
        accent = cfg.get("accent_color")
        if accent:
            setThemeColor(QColor(accent))

    @staticmethod
    def toggle_theme():
        current = cfg.get("dark_mode")
        cfg.set("dark_mode", not current)
        ThemeManager.apply_theme()
