from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor
from qfluentwidgets import (MessageBox, ColorPickerButton, SwitchButton, 
                            ComboBox, SubtitleLabel, CaptionLabel)
from config import cfg
from utils.theme_manager import ThemeManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(400, 300)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Appearance
        # Appearance
        self.appearance_group = QGroupBox("Appearance")
        self.appearance_layout = QFormLayout(self.appearance_group)
        
        self.theme_switch = SwitchButton(self)
        self.theme_switch.setChecked(cfg.get("dark_mode"))
        self.theme_switch.checkedChanged.connect(self.on_theme_changed)
        self.appearance_layout.addRow("Dark Mode:", self.theme_switch)
        
        try:
            self.color_picker = ColorPickerButton(QColor(cfg.get("accent_color")), "Accent Color", self)
            self.color_picker.colorChanged.connect(self.on_color_changed)
            self.appearance_layout.addRow("Accent Color:", self.color_picker)
        except Exception as e:
            print(f"Error initializing ColorPickerButton: {e}")
            self.color_label = SubtitleLabel("Color Picker Unavailable", self)
            self.appearance_layout.addRow("Accent Color:", self.color_label)
        
        self.layout.addWidget(self.appearance_group)
        
        # Search
        self.search_group = QGroupBox("Search")
        self.search_layout = QFormLayout(self.search_group)
        
        self.engine_combo = ComboBox(self)
        self.engine_combo.addItems(list(cfg.SEARCH_ENGINES.keys()))
        self.engine_combo.setCurrentText(cfg.get("search_engine"))
        self.engine_combo.currentTextChanged.connect(self.on_engine_changed)
        self.search_layout.addRow("Default Search Engine:", self.engine_combo)
        
        self.layout.addWidget(self.search_group)
        self.layout.addStretch()
        
    def on_theme_changed(self, checked):
        cfg.set("dark_mode", checked)
        ThemeManager.apply_theme()
        
    def on_color_changed(self, color):
        cfg.set("accent_color", color.name())
        ThemeManager.apply_theme()
        
    def on_engine_changed(self, text):
        cfg.set("search_engine", text)
