import hashlib
import os
import sys
from typing import Dict, List, Iterable, Optional

try:
    from tqdm import tqdm
    USE_TQDM = True
except ImportError:
    USE_TQDM = False


def compute_md5(path: str, blocksize: int = 65536) -> str:
    """Compute MD5 hash of a file using efficient chunk streaming."""
    try:
        with open(path, "rb") as file:
            try:
                # Python 3.11+ fast hashing
                return hashlib.file_digest(file, "md5").hexdigest()
            except AttributeError:
                hasher = hashlib.md5()
                for chunk in iter(lambda: file.read(blocksize), b""):
                    hasher.update(chunk)
                return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing file {path}: {e}")
        return ""


def scan_folder(folder: str) -> Dict[str, List[str]]:
    """Scan a folder recursively and group files by MD5 hash."""
    duplicates: Dict[str, List[str]] = {}
    files: List[str] = []

    for dirpath, _, filenames in os.walk(folder):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            files.append(full_path)

    iterator = tqdm(files, desc=f"Scanning {folder}") if USE_TQDM else files

    for path in iterator:
        file_hash = compute_md5(path)
        if not file_hash:
            continue
        duplicates.setdefault(file_hash, []).append(path)

    return duplicates


def merge_dicts(base: Dict[str, List[str]], new: Dict[str, List[str]]):
    """Merge dictionaries by appending lists for matching keys."""
    for key, paths in new.items():
        base.setdefault(key, []).extend(paths)


def delete_duplicates(duplicate_map: Dict[str, List[str]]):
    """Delete duplicate files, keeping only one per hash group."""
    for paths in duplicate_map.values():
        if len(paths) > 1:
            keep = paths[0]
            print(f"Keeping: {keep}")
            for dup in paths[1:]:
                try:
                    os.remove(dup)
                    print(f"Deleted: {dup}")
                except Exception as e:
                    print(f"Error deleting {dup}: {e}")


def print_results(duplicate_map: Dict[str, List[str]]):
    groups = [paths for paths in duplicate_map.values() if len(paths) > 1]

    if not groups:
        print("\nNo duplicate images found.")
        return

    print("\n===============================")
    print(" Duplicate Images Found")
    print("===============================\n")

    for group in groups:
        print("Group:")
        for file_path in group:
            print("   -", file_path)
        print("-------------------------------")


def confirm(prompt: str) -> bool:
    """Simple yes/no prompt."""
    choice = input(f"{prompt} (y/n): ").strip().lower()
    return choice == "y"


def main():
    if len(sys.argv) <= 1:
        print("Usage: python image_finder.py <folder1> <folder2> ...")
        return

    folders = sys.argv[1:]
    duplicate_map: Dict[str, List[str]] = {}

    for folder in folders:
        if not os.path.isdir(folder):
            print(f"Invalid folder: {folder}")
            continue

        print(f"\nProcessing folder: {folder}")
        data = scan_folder(folder)
        merge_dicts(duplicate_map, data)

    print_results(duplicate_map)

    if confirm("Delete duplicate images?"):
        delete_duplicates(duplicate_map)
        print("\nDuplicates deleted.")
    else:
        print("\nNo files were deleted.")


if __name__ == "__main__":
    main()
