from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from qfluentwidgets import ListWidget, PrimaryPushButton, PushButton
from config import cfg

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.resize(500, 400)
        
        self.layout = QVBoxLayout(self)
        
        self.list_widget = ListWidget(self)
        self.refresh_list()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.layout.addWidget(self.list_widget)
        
        self.btn_layout = QHBoxLayout()
        self.btn_clear = PushButton("Clear History", self)
        self.btn_clear.clicked.connect(self.clear_history)
        self.btn_open = PrimaryPushButton("Open", self)
        self.btn_open.clicked.connect(self.open_selected)
        
        self.btn_layout.addWidget(self.btn_clear)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn_open)
        
        self.layout.addLayout(self.btn_layout)
        
    def refresh_list(self):
        self.list_widget.clear()
        for item in cfg.get("history"):
            self.list_widget.addItem(f"{item['title']} - {item['url']}")
            
    def clear_history(self):
        cfg.clear_history()
        self.refresh_list()
        
    def open_selected(self):
        item = self.list_widget.currentItem()
        if item:
            self.on_item_double_clicked(item)
            
    def on_item_double_clicked(self, item):
        idx = self.list_widget.row(item)
        url = cfg.get("history")[idx]['url']
        if self.parent():
            self.parent().open_url(url)
        self.close()
