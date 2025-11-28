import json
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class Config(QObject):
    changed = pyqtSignal(str)  # Signal emitted when a setting changes

    def __init__(self):
        super().__init__()
        self.config_file = Path.home() / ".nhc_browser_config.json"
        self.SEARCH_ENGINES = {
            "Google": "https://www.google.com/search?q=",
            "Bing": "https://www.bing.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Yahoo": "https://search.yahoo.com/search?p=",
            "Startpage": "https://www.startpage.com/do/search?q=",
            "Ecosia": "https://www.ecosia.org/search?q="
        }
        self.defaults = {
            "dark_mode": False,
            "accent_color": "#009faa",
            "search_engine": "Google",
            "home_url": "nhc://start",
            "bookmarks": [],
            "history": []
        }
        self.data = self.defaults.copy()
        self.load()

    def load(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key):
        return self.data.get(key, self.defaults.get(key))

    def set(self, key, value):
        if self.data.get(key) != value:
            self.data[key] = value
            self.save()
            self.changed.emit(key)

    def add_bookmark(self, title, url):
        bookmarks = self.get("bookmarks")
        if not any(b['url'] == url for b in bookmarks):
            bookmarks.append({"title": title, "url": url})
            self.set("bookmarks", bookmarks)
            return True
        return False

    def remove_bookmark(self, index):
        bookmarks = self.get("bookmarks")
        if 0 <= index < len(bookmarks):
            del bookmarks[index]
            self.set("bookmarks", bookmarks)

    def add_history(self, title, url):
        if url == "about:blank" or url.startswith("nhc://"):
            return
        history = self.get("history")
        history.insert(0, {"title": title, "url": url})
        history = history[:100]  # Keep last 100
        self.set("history", history)

    def clear_history(self):
        self.set("history", [])

# Global instance
cfg = Config()
