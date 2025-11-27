<h1 align="center"> HandyPy </h1>
<h2 align="center"> 
<p align="center">
 <img alt="Languages" src="https://img.shields.io/github/languages/count/haiderCho/HandyPy">
 <img alt="Repository size" src="https://img.shields.io/github/repo-size/haiderCho/HandyPy">
 <img alt="Contributors" src="https://img.shields.io/github/contributors/haiderCho/HandyPy">
 <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/haiderCho/HandyPy">
</p>
</h2>

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## 📝 About

**HandyPy** is a comprehensive collection of **Python GUI applications** built with Tkinter and PyQt6. 
Each applet is self-contained in its own directory with specific documentation.

## 📂 Applet Directory

### 🧮 Calculators & Converters
| Applet | Description |
|--------|-------------|
| [**Advanced Calculator**](Calculator/) | Scientific calculator with secure AST-based evaluation |
| [**All-in-One Converter**](AIOConverter/) | Currency, weight, length, area, and temperature converter |
| [**Age Calculator**](AgeCalculator/) | Calculate exact age with detailed breakdown |
| [**BMI Calculator**](BMI-Calculator/) | Body Mass Index calculator with health classifications |
| [**Binary Calculator**](Binary-Calculator/) | Binary arithmetic and conversion tool |
| [**Distance Calculator**](DistanceCalculator/) | Calculate distance between locations |
| [**Distance Conversion**](DistanceConversion/) | Distance unit converter |

### 🛠️ Utilities
| Applet | Description |
|--------|-------------|
| [**Advanced Notepad**](Notepad/) | Feature-rich text editor with find/replace and stats |
| [**File Sorter**](FileSorter/) | Organize files by extension automatically |
| [**Duplicate File Finder**](DuplicateFileFinder/) | Find and remove duplicate files (CLI) |
| [**Duplicate Image Finder**](DuplicateImageFinder/) | Find duplicate images visually (GUI) |
| [**Password Generator**](PasswordGenerator/) | Secure password generator with strength indicator |
| [**QR Code Generator**](QRCodeGenerator/) | Generate and save custom QR codes |
| [**URL Shortener**](URLShortener/) | Shorten URLs with validation and clipboard support |
| [**Stopwatch**](Stopwatch/) | Precise stopwatch with lap timing |
| [**Calendar**](Calendar/) | Simple GUI calendar |

### 🌐 Internet & Language
| Applet | Description |
|--------|-------------|
| [**Epic Browser**](Browser/) | Modern PyQt6 web browser with tabs, bookmarks, and history |
| [**Translator**](Translator/) | Multi-language translator (90+ languages) |
| [**ChatBot**](ChatBot/) | Interactive rule-based chatbot |
| [**Dictionary**](Dictionary/) | Online word definitions and synonyms |
| [**Offline Dictionary**](OfflineDictionary/) | Local dictionary without internet requirement |

### 🎮 Development & Games
| Applet | Description |
|--------|-------------|
| [**Python IDE**](PythonIDE/) | Lightweight Python code editor and runner |
| [**Hangman**](HangMan/) | Classic word guessing game |
| [**Sorting Visualizer**](SortingAlgorithmVisualizer/) | Visualize sorting algorithms in real-time |

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/haiderCho/HandyPy.git
cd HandyPy
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run an applet**
Navigate to the folder and run the Python script:
```bash
cd Calculator
python Calculator.py
```

## 📦 Dependencies

Core dependencies are listed in `requirements.txt`. Key libraries include:
- `tkinter` (Standard GUI)
- `PyQt6` (Modern Browser)
- `Pillow` (Image processing)
- `deep-translator` (Translation)
- `qrcode` (QR generation)

## 🤝 Contributing

Contributions are welcome! Please check individual applet folders for specific details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
