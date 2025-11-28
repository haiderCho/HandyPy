from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from qfluentwidgets import ListWidget, PrimaryPushButton, PushButton
from config import cfg

class BookmarksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bookmarks")
        self.resize(500, 400)
        
        self.layout = QVBoxLayout(self)
        
        self.list_widget = ListWidget(self)
        self.refresh_list()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.layout.addWidget(self.list_widget)
        
        self.btn_layout = QHBoxLayout()
        self.btn_delete = PushButton("Delete", self)
        self.btn_delete.clicked.connect(self.delete_bookmark)
        self.btn_open = PrimaryPushButton("Open", self)
        self.btn_open.clicked.connect(self.open_selected)
        
        self.btn_layout.addWidget(self.btn_delete)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn_open)
        
        self.layout.addLayout(self.btn_layout)
        
    def refresh_list(self):
        self.list_widget.clear()
        for item in cfg.get("bookmarks"):
            self.list_widget.addItem(f"{item['title']} - {item['url']}")
            
    def delete_bookmark(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            cfg.remove_bookmark(row)
            self.refresh_list()
        
    def open_selected(self):
        item = self.list_widget.currentItem()
        if item:
            self.on_item_double_clicked(item)
            
    def on_item_double_clicked(self, item):
        idx = self.list_widget.row(item)
        url = cfg.get("bookmarks")[idx]['url']
        if self.parent():
            self.parent().open_url(url)
        self.close()
