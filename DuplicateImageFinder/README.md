# Duplicate Image Finder

A GUI tool to find and manage duplicate images.

## Features

- **Visual Comparison**: Shows thumbnails of duplicate images
- **Smart Detection**: Uses MD5 hashing for exact matches
- **Batch Actions**: Delete selected, Keep one, Move to folder
- **Export**: Save results to JSON
- **Progress**: Real-time scanning progress bar

## Usage

```bash
python DuplicateImageFinder.py
```

1. Select folder to scan
2. Wait for scan to complete
3. Review duplicates in the gallery view
4. Select actions for duplicates

## Requirements

- Python 3.6+
- Pillow (PIL)
- tkinter (built-in)
