from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from qfluentwidgets import SearchLineEdit, ComboBox, TitleLabel, BodyLabel
from config import cfg

class StartPage(QWidget):
    """Custom Start Page"""
    
    search_requested = pyqtSignal(str) # Signal to request search/navigation
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)
        
        # Title
        self.title = TitleLabel("NHC Browser", self)
        self.title.setStyleSheet("font-size: 48px; font-weight: bold;")
        
        # Search Box
        self.search_box = SearchLineEdit(self)
        self.search_box.setPlaceholderText("Search the web...")
        self.search_box.setFixedWidth(600)
        self.search_box.returnPressed.connect(self.on_search)
        self.search_box.searchButton.clicked.connect(self.on_search)
        
        # Search Engine Selector
        self.engine_layout = QHBoxLayout()
        self.engine_label = BodyLabel("Search Engine:", self)
        self.engine_combo = ComboBox(self)
        self.engine_combo.addItems(list(cfg.SEARCH_ENGINES.keys()))
        self.engine_combo.setCurrentText(cfg.get("search_engine"))
        self.engine_combo.currentTextChanged.connect(self.on_engine_changed)
        
        self.engine_layout.addWidget(self.engine_label)
        self.engine_layout.addWidget(self.engine_combo)
        self.engine_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add to layout
        self.layout.addStretch()
        self.layout.addWidget(self.title, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.search_box, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.engine_layout)
        self.layout.addStretch()
        
    def on_search(self):
        text = self.search_box.text()
        if text:
            self.search_requested.emit(text)
            
    def on_engine_changed(self, text):
        cfg.set("search_engine", text)
