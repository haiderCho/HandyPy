# NHC Browser - User Guide

## Overview
NHC Browser is a modern, feature-rich web browser built with PyQt6, Qt WebEngine (Chromium-based), and PyQt-Fluent-Widgets. It provides a fast, secure browsing experience with a beautiful Fluent Design interface.

## Features

### 🔖 Multiple Tabs
- **New Tab**: Click the `+` button or press `Ctrl+T`
- **Close Tab**: Click the × on the tab or press `Ctrl+W`
- **Switch Tabs**: Click on tabs or use mouse wheel
- **Reorder Tabs**: Drag and drop tabs to reorder

### ⭐ Bookmarks
- **Add Bookmark**: Click the ★ button or press `Ctrl+D`
- **View All Bookmarks**: Menu → Bookmarks → Show All Bookmarks
- **Open Bookmark**: Double-click in bookmarks dialog or select from menu
- **Delete Bookmark**: Select and click Delete in bookmarks dialog
- **Quick Access**: First 10 bookmarks appear in Bookmarks menu

### 📜 Browsing History
- **View History**: Press `Ctrl+H` or Menu → History → Show History
- **Open from History**: Double-click any entry
- **Clear History**: Menu → History → Clear History
- **Auto-save**: Last 100 visited pages are automatically saved

### 🎨 Themes
- **Toggle Theme**: Press `Ctrl+D` or Menu → View → Toggle Dark Mode
- **Dark Mode**: Professional dark theme for nighttime browsing
- **Light Mode**: Clean, bright theme for daytime use
- **Persistent**: Theme preference is saved between sessions

### 🔍 Navigation
- **Back/Forward**: Use ← and → buttons or browser shortcuts
- **Reload**: Click ↻ button or press F5
- **Home**: Click ⌂ button to return to the Start Page
- **Stop Loading**: Click Stop button

### 🔎 Smart URL Bar
- **Enter URLs**: Type any URL (http:// added automatically)
- **Search**: Type search queries directly (uses your selected search engine)
- **Auto-complete**: Shows current page URL

### 🔬 Zoom Controls
- **Zoom In**: Press `Ctrl++` or Menu → View → Zoom In
- **Zoom Out**: Press `Ctrl+-` or Menu → View → Zoom Out
- **Reset Zoom**: Press `Ctrl+0` or Menu → View → Reset Zoom
- **Range**: 25% to 500%
- **Status Display**: Zoom percentage shown in status bar

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | New Tab |
| `Ctrl+W` | Close Current Tab |
| `Ctrl+D` | Toggle Dark Mode / Add Bookmark |
| `Ctrl+H` | Show History |
| `Ctrl+Q` | Quit Browser |
| `Ctrl++` | Zoom In |
| `Ctrl+-` | Zoom Out |
| `Ctrl+0` | Reset Zoom |
| `F5` | Reload Page |

### 💾 Settings Persistence
All your preferences are automatically saved:
- **Bookmarks**: Saved permanently
- **History**: Last 100 pages
- **Theme**: Dark/Light preference
- **Location**: `~/.nhc_browser_config.json`

## Usage Tips

### Adding Multiple Tabs
1. Press `Ctrl+T` to open a new tab
2. Or click the `+` button in the toolbar
3. Each tab has independent browsing

### Managing Bookmarks
1. Navigate to a page you like
2. Click the ★ button or press `Ctrl+D`
3. Access from Bookmarks menu or bookmarks manager
4. Organize by opening bookmarks dialog

### Searching the Web
Just type your search query in the URL bar:
- Type: `python tutorials`
- Press Enter
- Automatically searches using your default search engine (Google, Bing, DuckDuckGo, Yahoo, Startpage, or Ecosia)

### Customizing Appearance
- Toggle between dark and light themes instantly
- Dark mode is perfect for late-night browsing
- Light mode for daytime use

## Technical Details

**Browser Engine**: Qt WebEngine (Chromium-based)
**Framework**: PyQt6 & PyQt-Fluent-Widgets
**Configuration**: JSON file in home directory
**History Limit**: 100 most recent pages
**Bookmark Limit**: Unlimited (10 shown in menu)

## Troubleshooting

**Browser won't start?**
- Ensure PyQt6, PyQt6-WebEngine, and PyQt-Fluent-Widgets are installed
- Run: `pip install PyQt6 PyQt6-WebEngine "PyQt-Fluent-Widgets[full]"`

**Bookmarks not saving?**
- Check write permissions in home directory
- Config file: `~/.nhc_browser_config.json`

**Slow performance?**
- Reduce number of open tabs
- Clear browsing history
- Check zoom level (reset with Ctrl+0)

## Privacy

- **History**: Stored locally only, last 100 pages
- **Bookmarks**: Stored locally only
- **No Tracking**: NHC Browser does not track you
- **Clear Data**: Use History → Clear History to remove all history

---

Enjoy browsing with NHC Browser! 🚀
