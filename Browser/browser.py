# importing required libraries
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
import sys
import json
from pathlib import Path

# Browser Tab Widget
class BrowserTab(QWidget):
    """Individual browser tab with its own webview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        
    def get_browser(self):
        return self.browser

# Main Browser Window
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NHC Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Settings
        self.bookmarks = []
        self.history = []
        self.dark_mode = False
        self.config_file = Path.home() / ".nhc_browser_config.json"
        self.load_settings()
        
        # UI Components
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        
        # Set tab bar to top with modern styling
        self.tabs.setDocumentMode(True)
        
        self.setCentralWidget(self.tabs)
        
        # Create navigation toolbar
        self.create_navbar()
        
        # Create menu bar
        self.create_menubar()
        
        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        # Apply initial theme
        self.apply_theme()
        
        # Add first tab
        self.add_new_tab(QUrl("https://www.google.com"), "Home")
        
        self.show()
    
    def create_navbar(self):
        """Create modern navigation toolbar"""
        navbar = QToolBar("Navigation")
        navbar.setIconSize(QSize(24, 24))
        navbar.setMovable(False)
        self.addToolBar(navbar)
        
        # Back button
        back_btn = QAction("←", self)
        back_btn.setStatusTip("Back")
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)
        
        # Forward button
        forward_btn = QAction("→", self)
        forward_btn.setStatusTip("Forward")
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)
        
        # Reload button
        reload_btn = QAction("↻", self)
        reload_btn.setStatusTip("Reload")
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)
        
        # Home button
        home_btn = QAction("⌂", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        navbar.addSeparator()
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Enter URL or search...")
        navbar.addWidget(self.url_bar)
        
        navbar.addSeparator()
        
        # Bookmark button
        bookmark_btn = QAction("★", self)
        bookmark_btn.setStatusTip("Bookmark this page")
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)
        
        # New tab button
        new_tab_btn = QAction("+", self)
        new_tab_btn.setStatusTip("New Tab")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(new_tab_btn)
    
    def create_menubar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)
        
        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        theme_action = QAction("Toggle Dark Mode", self)
        theme_action.setShortcut("Ctrl+D")
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(lambda: self.zoom_page(0.1))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(lambda: self.zoom_page(-0.1))
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(lambda: self.current_browser().setZoomFactor(1.0))
        view_menu.addAction(reset_zoom_action)
        
        # Bookmarks menu
        bookmarks_menu = menubar.addMenu("&Bookmarks")
        
        add_bookmark_action = QAction("Bookmark This Page", self)
        add_bookmark_action.setShortcut("Ctrl+D")
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)
        
        show_bookmarks_action = QAction("Show All Bookmarks", self)
        show_bookmarks_action.triggered.connect(self.show_bookmarks)
        bookmarks_menu.addAction(show_bookmarks_action)
        
        bookmarks_menu.addSeparator()
        
        # Add bookmarks to menu
        self.bookmarks_menu = bookmarks_menu
        self.update_bookmarks_menu()
        
        # History menu
        history_menu = menubar.addMenu("&History")
        
        show_history_action = QAction("Show History", self)
        show_history_action.setShortcut("Ctrl+H")
        show_history_action.triggered.connect(self.show_history)
        history_menu.addAction(show_history_action)
        
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def add_new_tab(self, qurl=None, label="New Tab"):
        """Add a new tab"""
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        
        # Create new tab
        browser_tab = BrowserTab()
        browser = browser_tab.get_browser()
        
        # Connect signals
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=self.tabs.count(), browser=browser:
                                    self.tabs.setTabText(i, browser.page().title()[:20]))
        browser.loadFinished.connect(lambda: self.add_to_history(browser.url()))
        
        # Add tab
        i = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(i)
        
        # Navigate to URL
        if qurl:
            browser.setUrl(qurl)
        
        return browser
    
    def close_tab(self, i):
        """Close a tab"""
        if self.tabs.count() < 2:
            return
        
        self.tabs.removeTab(i)
    
    def current_browser(self):
        """Get current browser widget"""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            return current_tab.get_browser()
        return None
    
    def current_tab_changed(self, i):
        """Update URL bar when tab changes"""
        browser = self.current_browser()
        if browser:
            qurl = browser.url()
            self.update_url(qurl, browser)
    
    def update_url(self, q, browser=None):
        """Update URL bar"""
        if browser != self.current_browser():
            return
        
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
    
    def navigate_to_url(self):
        """Navigate to URL in URL bar"""
        url = self.url_bar.text()
        
        # Check if it's a search query or URL
        if " " in url or "." not in url:
            url = "https://www.google.com/search?q=" + url
        elif not url.startswith("http"):
            url = "https://" + url
        
        self.current_browser().setUrl(QUrl(url))
    
    def navigate_home(self):
        """Navigate to home page"""
        self.current_browser().setUrl(QUrl("https://www.google.com"))
    
    def add_bookmark(self):
        """Add current page to bookmarks"""
        browser = self.current_browser()
        if browser:
            url = browser.url().toString()
            title = browser.page().title()
            
            # Check if already bookmarked
            if any(b['url'] == url for b in self.bookmarks):
                QMessageBox.information(self, "Already Bookmarked", "This page is already in your bookmarks!")
                return
            
            self.bookmarks.append({"title": title, "url": url})
            self.save_settings()
            self.update_bookmarks_menu()
            QMessageBox.information(self, "Bookmarked", f"Added '{title}' to bookmarks!")
    
    def update_bookmarks_menu(self):
        """Update bookmarks in menu"""
        # Clear existing bookmark actions
        actions = self.bookmarks_menu.actions()
        for action in actions[3:]:  # Keep first 3 (Add, Show All, Separator)
            self.bookmarks_menu.removeAction(action)
        
        # Add bookmarks
        for bookmark in self.bookmarks[:10]:  # Show max 10 in menu
            action = QAction(bookmark['title'][:40], self)
            action.triggered.connect(lambda checked, url=bookmark['url']: 
                                    self.current_browser().setUrl(QUrl(url)))
            self.bookmarks_menu.addAction(action)
    
    def show_bookmarks(self):
        """Show bookmarks dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # Bookmarks list
        list_widget = QListWidget()
        for bookmark in self.bookmarks:
            list_widget.addItem(f"{bookmark['title']} - {bookmark['url']}")
        
        list_widget.itemDoubleClicked.connect(lambda item: self.open_bookmark_from_list(item))
        layout.addWidget(list_widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(lambda: self.open_bookmark_from_list(list_widget.currentItem()))
        btn_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.delete_bookmark(list_widget))
        btn_layout.addWidget(delete_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def open_bookmark_from_list(self, item):
        """Open bookmark from list"""
        if item:
            idx = item.listWidget().row(item)
            url = self.bookmarks[idx]['url']
            self.current_browser().setUrl(QUrl(url))
    
    def delete_bookmark(self, list_widget):
        """Delete selected bookmark"""
        current_item = list_widget.currentItem()
        if current_item:
            idx = list_widget.row(current_item)
            del self.bookmarks[idx]
            list_widget.takeItem(idx)
            self.save_settings()
            self.update_bookmarks_menu()
    
    def add_to_history(self, qurl):
        """Add URL to history"""
        url = qurl.toString()
        if url and url != "about:blank":
            self.history.insert(0, {"url": url, "title": self.current_browser().page().title()})
            self.history = self.history[:100]  # Keep last 100
            self.save_settings()
    
    def show_history(self):
        """Show browsing history"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Browsing History")
        dialog.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout()
        
        # History list
        list_widget = QListWidget()
        for entry in self.history:
            list_widget.addItem(f"{entry.get('title', 'Untitled')} - {entry['url']}")
        
        list_widget.itemDoubleClicked.connect(lambda item: self.open_history_item(item))
        layout.addWidget(list_widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(lambda: self.open_history_item(list_widget.currentItem()))
        btn_layout.addWidget(open_btn)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(lambda: self.clear_history_confirm(list_widget, dialog))
        btn_layout.addWidget(clear_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        dialog.setLayout(layout)
        dialog.exec()
    
    def open_history_item(self, item):
        """Open URL from history"""
        if item:
            idx = item.listWidget().row(item)
            url = self.history[idx]['url']
            self.current_browser().setUrl(QUrl(url))
    
    def clear_history(self):
        """Clear browsing history"""
        self.history = []
        self.save_settings()
        QMessageBox.information(self, "History Cleared", "Browsing history has been cleared!")
    
    def clear_history_confirm(self, list_widget, dialog):
        """Clear history with confirmation"""
        reply = QMessageBox.question(self, "Clear History", 
                                     "Are you sure you want to clear all history?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_history()
            list_widget.clear()
            dialog.close()
    
    def toggle_theme(self):
        """Toggle dark/light theme"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.save_settings()
    
    def apply_theme(self):
        """Apply current theme"""
        if self.dark_mode:
            # Dark theme
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QToolBar {
                    background-color: #3c3c3c;
                    border: none;
                    spacing: 5px;
                    padding: 5px;
                }
                QLineEdit {
                    background-color: #4a4a4a;
                    color: #ffffff;
                    border: 1px solid #666666;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 1px solid #007acc;
                }
                QPushButton {
                    background-color: #4a4a4a;
                    color: #ffffff;
                    border: 1px solid #666666;
                    border-radius: 4px;
                    padding: 6px 16px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #5a5a5a;
                }
                QPushButton:pressed {
                    background-color: #3a3a3a;
                }
                QTabWidget::pane {
                    border: 1px solid #444444;
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    padding: 8px 16px;
                    border: 1px solid #444444;
                    border-bottom: none;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background-color: #2b2b2b;
                }
                QTabBar::tab:hover {
                    background-color: #4a4a4a;
                }
                QMenuBar {
                    background-color: #3c3c3c;
                    color: #ffffff;
                }
                QMenuBar::item:selected {
                    background-color: #4a4a4a;
                }
                QMenu {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #666666;
                }
                QMenu::item:selected {
                    background-color: #4a4a4a;
                }
                QStatusBar {
                    background-color: #3c3c3c;
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: 1px solid #444444;
                }
                QListWidget::item:selected {
                    background-color: #007acc;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QToolBar {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    spacing: 5px;
                    padding: 5px;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 1px solid #007acc;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 6px 16px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QTabWidget::pane {
                    border: 1px solid #c0c0c0;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #e0e0e0;
                    color: #000000;
                    padding: 8px 16px;
                    border: 1px solid #c0c0c0;
                    border-bottom: none;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background-color: #ffffff;
                }
                QTabBar::tab:hover {
                    background-color: #f0f0f0;
                }
                QMenuBar {
                    background-color: #ffffff;
                    color: #000000;
                }
                QMenuBar::item:selected {
                    background-color: #e8e8e8;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #c0c0c0;
                }
                QMenu::item:selected {
                    background-color: #e8e8e8;
                }
                QStatusBar {
                    background-color: #ffffff;
                    color: #000000;
                    border-top: 1px solid #c0c0c0;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #c0c0c0;
                }
                QListWidget::item:selected {
                    background-color: #007acc;
                    color: #ffffff;
                }
            """)
    
    def zoom_page(self, delta):
        """Zoom current page"""
        browser = self.current_browser()
        if browser:
            current_zoom = browser.zoomFactor()
            new_zoom = max(0.25, min(5.0, current_zoom + delta))
            browser.setZoomFactor(new_zoom)
            self.status.showMessage(f"Zoom: {int(new_zoom * 100)}%", 2000)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About NHC Browser",
                         "<h2>NHC Browser</h2>"
                         "<p>A modern, feature-rich web browser built with PyQt6</p>"
                         "<p><b>Features:</b></p>"
                         "<ul>"
                         "<li>Multiple tabs</li>"
                         "<li>Bookmarks manager</li>"
                         "<li>Browsing history</li>"
                         "<li>Dark/Light theme</li>"
                         "<li>Zoom control</li>"
                         "<li>Keyboard shortcuts</li>"
                         "</ul>"
                         "<p>Powered by Qt WebEngine (Chromium)</p>")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.bookmarks = data.get('bookmarks', [])
                    self.history = data.get('history', [])
                    self.dark_mode = data.get('dark_mode', False)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            data = {
                'bookmarks': self.bookmarks,
                'history': self.history,
                'dark_mode': self.dark_mode
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def closeEvent(self, event):
        """Save settings before closing"""
        self.save_settings()
        event.accept()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("NHC Browser")
    app.setOrganizationName("NHC")
    
    window = MainWindow()
    
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing application...")
