# Duplicate File Finder

A command-line tool to find and remove duplicate files.

## Features

- **MD5 Hashing**: Accurate duplicate detection based on content, not just name
- **Recursive Search**: Scans subdirectories
- **Safety**: Prompts before deletion
- **Performance**: Efficient scanning of large directories

## Usage

```bash
python DuplicateFileFinder.py <folder_path> [folder_path2 ...]
```

Example:
```bash
python DuplicateFileFinder.py C:\Users\Photos
```

## How it Works

1. Scans all files in provided directories
2. Calculates MD5 hash of files
3. Identifies duplicates with identical hashes
4. Keeps the first instance and lists duplicates for removal

## Requirements

- Python 3.6+
