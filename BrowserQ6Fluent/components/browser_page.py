from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import QWebEngineSettings
from qfluentwidgets import ToolButton, LineEdit, FluentIcon as FIF
from config import cfg
from components.start_page import StartPage

class BrowserPage(QWidget):
    """Individual browser page with navigation and webview"""
    
    def __init__(self, url=None, parent=None):
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
        
        # Stacked Widget for Web/Start
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # WebView
        self.browser = QWebEngineView()
        self.stack.addWidget(self.browser)
        
        # Start Page
        self.start_page = StartPage()
        self.start_page.search_requested.connect(self.process_url)
        self.stack.addWidget(self.start_page)
        
        # Connections
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)
        self.btn_reload.clicked.connect(self.browser.reload)
        self.btn_home.clicked.connect(self.go_home)
        
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.on_load_finished)
        
        # Initial Load
        if url:
            self.load_url(url)
        else:
            self.go_home()
            
        # Security & UI
        self.configure_security()
        self.setStyleSheet("background-color: transparent;")

    def configure_security(self):
        settings = self.browser.settings()
        # Security options
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, False)
        
        # Optional: Set user agent or other profile settings if needed
        # profile = self.browser.page().profile()
        # profile.setHttpUserAgent("NHC Browser/1.0")

    def load_url(self, url):
        if url == "nhc://start":
            self.stack.setCurrentWidget(self.start_page)
            self.url_bar.clear()
            self.url_bar.setPlaceholderText("Search or enter address")
        else:
            self.stack.setCurrentWidget(self.browser)
            self.browser.setUrl(QUrl(url))

    def navigate(self):
        url = self.url_bar.text()
        self.process_url(url)

    def process_url(self, url):
        if not url:
            return
            
        if url == "nhc://start":
            self.load_url(url)
            return

        # Check if it's a search query or URL
        if " " in url or "." not in url:
            engine = cfg.get("search_engine")
            base_url = cfg.SEARCH_ENGINES.get(engine, cfg.SEARCH_ENGINES["Google"])
            url = base_url + url
        elif not url.startswith("http"):
            url = "https://" + url
        
        self.load_url(url)

    def go_home(self):
        home_url = cfg.get("home_url")
        self.load_url(home_url)

    def update_url(self, qurl):
        if self.stack.currentWidget() == self.browser:
            self.url_bar.setText(qurl.toString())
            self.url_bar.setCursorPosition(0)
        
    def on_load_finished(self):
        if self.stack.currentWidget() == self.browser:
            title = self.browser.page().title()
            url = self.browser.url().toString()
            cfg.add_history(title, url)
