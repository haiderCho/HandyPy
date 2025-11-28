import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from qfluentwidgets import (FluentWindow, TabBar, FluentIcon as FIF, 
                            TabCloseButtonDisplayMode, NavigationItemPosition)

from config import cfg
from utils.theme_manager import ThemeManager
from components.browser_page import BrowserPage
from dialogs.settings_dialog import SettingsDialog
from dialogs.history_dialog import HistoryDialog
from dialogs.bookmarks_dialog import BookmarksDialog

class MainWindow(FluentWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NHC Browser")
        self.resize(1200, 800)
        
        # Hide default navigation interface
        self.navigationInterface.hide()
        
        # Main Layout
        self.main_widget = QWidget()
        self.main_widget.setObjectName("NHC Browser")
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Top Bar (Menu + Tabs)
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(40)
        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(5, 0, 5, 0)
        self.top_layout.setSpacing(5)
        
        # Menu Button
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setFixedSize(30, 30)
        self.menu_btn.clicked.connect(self.show_menu)
        self.top_layout.addWidget(self.menu_btn)
        
        # Tab Bar
        self.tab_bar = TabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabMaximumWidth(200)
        self.tab_bar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ALWAYS)
        self.tab_bar.currentChanged.connect(self.on_tab_changed)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.tabAddRequested.connect(self.add_new_tab)
        
        self.top_layout.addWidget(self.tab_bar, 1)
        
        self.main_layout.addWidget(self.top_bar)
        
        # Stacked Widget for Tabs
        self.stacked_widget = QStackedWidget(self)
        self.main_layout.addWidget(self.stacked_widget)
        
        # Set as central widget
        self.addSubInterface(self.main_widget, FIF.GLOBE, "Browser")
        
        # Initial Tab
        self.add_new_tab()
        
        # Theme
        ThemeManager.apply_theme()

    def add_new_tab(self):
        page = BrowserPage()
        key = str(id(page))
        
        # Connect title change
        page.browser.loadFinished.connect(lambda: self.update_tab_title(page))
        
        self.stacked_widget.addWidget(page)
        self.tab_bar.addTab(key, "New Tab", FIF.GLOBE)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        
    def close_tab(self, index):
        if self.tab_bar.count() <= 1:
            self.close()
            return

        widget = self.stacked_widget.widget(index)
        self.tab_bar.removeTab(index)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()

    def update_tab_title(self, page):
        title = page.browser.page().title()
        if len(title) > 20:
            title = title[:20] + "..."
            
        index = self.stacked_widget.indexOf(page)
        if index != -1:
            self.tab_bar.setTabText(index, title)

    def on_tab_changed(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
    def show_menu(self):
        menu = QMenu(self)
        
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        menu.addAction(new_tab_action)
        
        menu.addSeparator()
        
        bookmarks_action = QAction("Bookmarks", self)
        bookmarks_action.triggered.connect(self.show_bookmarks)
        menu.addAction(bookmarks_action)
        
        add_bookmark_action = QAction("Bookmark This Page", self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        menu.addAction(add_bookmark_action)
        
        history_action = QAction("History", self)
        history_action.triggered.connect(self.show_history)
        menu.addAction(history_action)
        
        menu.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.exec(self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height())))

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
        
    def show_history(self):
        dialog = HistoryDialog(self)
        dialog.exec()
        
    def show_bookmarks(self):
        dialog = BookmarksDialog(self)
        dialog.exec()
        
    def add_bookmark(self):
        current_page = self.stacked_widget.currentWidget()
        if isinstance(current_page, BrowserPage):
            url = current_page.browser.url().toString()
            title = current_page.browser.page().title()
            if url and url != "about:blank" and not url.startswith("nhc://"):
                if cfg.add_bookmark(title, url):
                    QMessageBox.information(self, "Bookmarked", f"Added '{title}' to bookmarks!")
                else:
                    QMessageBox.information(self, "Already Bookmarked", "This page is already in your bookmarks!")

    def open_url(self, url):
        current_page = self.stacked_widget.currentWidget()
        if isinstance(current_page, BrowserPage):
            current_page.load_url(url)
        else:
            self.add_new_tab()
            self.stacked_widget.currentWidget().load_url(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
