import sys
import json
from pathlib import Path
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *

from qfluentwidgets import (FluentWindow, TabBar, LineEdit, ToolButton, 
                            FluentIcon as FIF, NavigationItemPosition, 
                            MessageBox, setTheme, Theme, qconfig,
                            TabCloseButtonDisplayMode)

class BrowserPage(QWidget):
    """Individual browser page with navigation and webview"""
    
    def __init__(self, url="https://www.google.com", parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Navigation Bar
        self.navbar = QWidget()
        self.navbar.setFixedHeight(50)
        self.navbar.setStyleSheet("background-color: transparent;")
        self.nav_layout = QHBoxLayout(self.navbar)
        self.nav_layout.setContentsMargins(10, 5, 10, 5)
        self.nav_layout.setSpacing(10)
        
        # Controls
        self.btn_back = ToolButton(FIF.LEFT_ARROW, self)
        self.btn_forward = ToolButton(FIF.RIGHT_ARROW, self)
        self.btn_reload = ToolButton(FIF.SYNC, self)
        self.btn_home = ToolButton(FIF.HOME, self)
        
        self.url_bar = LineEdit()
        self.url_bar.setPlaceholderText("Search or enter address")
        self.url_bar.returnPressed.connect(self.navigate)
        
        self.nav_layout.addWidget(self.btn_back)
        self.nav_layout.addWidget(self.btn_forward)
        self.nav_layout.addWidget(self.btn_reload)
        self.nav_layout.addWidget(self.btn_home)
        self.nav_layout.addWidget(self.url_bar, 1)
        
        self.layout.addWidget(self.navbar)
        
        # WebView
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)
        
        # Connections
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)
        self.btn_reload.clicked.connect(self.browser.reload)
        self.btn_home.clicked.connect(lambda: self.browser.setUrl(QUrl("https://www.google.com")))
        
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_title)
        
        # Initial Load
        self.browser.setUrl(QUrl(url))

    def navigate(self):
        url = self.url_bar.text()
        if " " in url or "." not in url:
            url = "https://www.google.com/search?q=" + url
        elif not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)
        
    def update_title(self):
        pass

class MainWindow(FluentWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NHC Browser")
        self.resize(1200, 800)
        
        # Configuration
        self.config_file = Path.home() / ".nhc_browser_config.json"
        
        # Hide default navigation interface as we are building a browser
        self.navigationInterface.hide()
        
        # Main Layout
        self.main_widget = QWidget()
        self.main_widget.setObjectName("NHC Browser")
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Tab Bar
        self.tab_bar = TabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabMaximumWidth(200)
        self.tab_bar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ALWAYS)
        self.tab_bar.currentChanged.connect(self.on_tab_changed)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.tabAddRequested.connect(self.add_new_tab)
        
        # Stacked Widget
        self.stacked_widget = QStackedWidget(self)
        
        self.main_layout.addWidget(self.tab_bar)
        self.main_layout.addWidget(self.stacked_widget)
        
        # Set as central widget (FluentWindow uses stacked widget internally, but we can set a sub interface)
        self.addSubInterface(self.main_widget, FIF.GLOBE, "Browser")
        
        # Initial Tab
        self.add_new_tab()
        
        # Theme
        self.load_settings()

    def add_new_tab(self):
        page = BrowserPage()
        key = str(id(page))
        
        # Connect title change
        page.browser.loadFinished.connect(lambda: self.update_tab_title(page))
        
        self.stacked_widget.addWidget(page)
        self.tab_bar.addTab(key, "New Tab", FIF.GLOBE)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        
    def close_tab(self, index):
        widget = self.stacked_widget.widget(index)
        
        self.tab_bar.removeTab(index)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()
        
        if self.tab_bar.count() == 0:
            self.close()

    def update_tab_title(self, page):
        title = page.browser.page().title()
        if len(title) > 20:
            title = title[:20] + "..."
            
        index = self.stacked_widget.indexOf(page)
        if index != -1:
            self.tab_bar.setTabText(index, title)

    def on_tab_changed(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def load_settings(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    if data.get('dark_mode', False):
                        setTheme(Theme.DARK)
                    else:
                        setTheme(Theme.LIGHT)
        except:
            pass

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
