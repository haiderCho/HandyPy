"""
Image Finder GUI
Features:
- Tkinter GUI (folder chooser, start/stop scan)
- Multi-threaded hashing using ThreadPoolExecutor
- Thumbnail preview (Pillow required)
- Policies to keep newest/oldest/largest/smallest or manual selection
- Progress bar and cancel support
- Export report (JSON)

Dependencies:
- Python 3.8+
- Pillow (pip install pillow)

Run:
python image_finder_gui.py

"""

import hashlib
import os
import sys
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception as e:
    print("Tkinter is required to run this GUI. Error:", e)
    sys.exit(1)

try:
    from PIL import Image, ImageTk
except Exception:
    print("Pillow is required. Install with: pip install pillow")
    sys.exit(1)

# -----------------------------
# Utilities
# -----------------------------

def compute_md5(path: str, blocksize: int = 65536) -> str:
    """Compute MD5 hash of a file. Returns empty string on error."""
    try:
        with open(path, "rb") as f:
            hasher = hashlib.md5()
            for chunk in iter(lambda: f.read(blocksize), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""


def file_info(path: str) -> Dict:
    st = os.stat(path)
    return {
        "path": path,
        "size": st.st_size,
        "mtime": st.st_mtime,
        "ctime": st.st_ctime,
    }


# -----------------------------
# Worker: scanning & hashing
# -----------------------------

class Scanner:
    def __init__(self, max_workers: int = 8):
        self._cancel = threading.Event()
        self.max_workers = max_workers

    def cancel(self):
        self._cancel.set()

    def reset(self):
        self._cancel.clear()

    def is_cancelled(self):
        return self._cancel.is_set()

    def gather_files(self, folders: List[str], include_exts: List[str] = None) -> List[str]:
        files = []
        for folder in folders:
            for dirpath, _, filenames in os.walk(folder):
                for name in filenames:
                    if include_exts:
                        if not any(name.lower().endswith(ext) for ext in include_exts):
                            continue
                    files.append(os.path.join(dirpath, name))
        return files

    def scan(self, folders: List[str], progress_callback=None, include_exts: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Returns mapping: md5 -> list of file_info dicts
        progress_callback(current, total) invoked if provided
        """
        self.reset()
        files = self.gather_files(folders, include_exts)
        total = len(files)
        result: Dict[str, List[Dict]] = {}

        if total == 0:
            return result

        # ThreadPoolExecutor for hashing
        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            future_to_path = {exe.submit(compute_md5, p): p for p in files}
            processed = 0
            for future in as_completed(future_to_path):
                if self.is_cancelled():
                    break
                path = future_to_path[future]
                md5 = future.result()
                if md5:
                    info = file_info(path)
                    result.setdefault(md5, []).append(info)
                processed += 1
                if progress_callback:
                    try:
                        progress_callback(processed, total)
                    except Exception:
                        pass

        return result


# -----------------------------
# GUI
# -----------------------------

THUMB_SIZE = (120, 90)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Duplicate Image Finder")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.scanner = Scanner(max_workers=8)
        self.duplicate_map: Dict[str, List[Dict]] = {}
        self.thumbs_cache: Dict[str, ImageTk.PhotoImage] = {}

        self.selected_folders: List[str] = []

        self.create_widgets()

    def create_widgets(self):
        # Top frame - folder selection and controls
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=8)

        self.folder_label = ttk.Label(top, text="No folders selected")
        self.folder_label.pack(side=tk.LEFT, padx=(2, 10))

        ttk.Button(top, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Clear Folders", command=self.clear_folders).pack(side=tk.LEFT, padx=4)

        ttk.Button(top, text="Start Scan", command=self.start_scan).pack(side=tk.LEFT, padx=8)
        ttk.Button(top, text="Cancel Scan", command=self.cancel_scan).pack(side=tk.LEFT, padx=4)

        # Policy
        policy_frame = ttk.LabelFrame(top, text="Keep Policy")
        policy_frame.pack(side=tk.LEFT, padx=12)
        self.policy_var = tk.StringVar(value="keep_newest")
        ttk.Radiobutton(policy_frame, text="Keep Newest", variable=self.policy_var, value="keep_newest").pack(side=tk.LEFT)
        ttk.Radiobutton(policy_frame, text="Keep Oldest", variable=self.policy_var, value="keep_oldest").pack(side=tk.LEFT)
        ttk.Radiobutton(policy_frame, text="Keep Largest", variable=self.policy_var, value="keep_largest").pack(side=tk.LEFT)
        ttk.Radiobutton(policy_frame, text="Keep Smallest", variable=self.policy_var, value="keep_smallest").pack(side=tk.LEFT)
        ttk.Radiobutton(policy_frame, text="Manual", variable=self.policy_var, value="manual").pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill=tk.X, padx=8, pady=(0,8))

        # Main panes
        main_pane = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Left - duplicate groups list
        left_frame = ttk.Frame(main_pane, width=380)
        main_pane.add(left_frame, weight=1)

        left_top = ttk.Frame(left_frame)
        left_top.pack(fill=tk.X)
        ttk.Label(left_top, text="Duplicate Groups").pack(side=tk.LEFT)
        ttk.Button(left_top, text="Export Report", command=self.export_report).pack(side=tk.RIGHT)

        self.groups_tree = ttk.Treeview(left_frame, columns=("count",), show="headings", selectmode="browse")
        self.groups_tree.heading("count", text="Count")
        self.groups_tree.column("count", width=60, anchor=tk.CENTER)
        self.groups_tree.pack(fill=tk.BOTH, expand=True)
        self.groups_tree.bind("<<TreeviewSelect>>", self.on_group_select)

        # Right - thumbnails and details
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=3)

        details_top = ttk.Frame(right_frame)
        details_top.pack(fill=tk.X)
        ttk.Label(details_top, text="Group Preview").pack(side=tk.LEFT)
        ttk.Button(details_top, text="Delete Selected/Policy", command=self.delete_by_policy).pack(side=tk.RIGHT)

        # Canvas for thumbnails with a scrollbar
        canvas_frame = ttk.Frame(right_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, background="#f6f6f6")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vscroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=vscroll.set)

        self.thumb_container = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.thumb_container, anchor="nw")
        self.thumb_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            if folder not in self.selected_folders:
                self.selected_folders.append(folder)
            self.folder_label.config(text="; ".join(self.selected_folders))

    def clear_folders(self):
        self.selected_folders = []
        self.folder_label.config(text="No folders selected")

    def start_scan(self):
        if not self.selected_folders:
            messagebox.showwarning("No folders", "Please add at least one folder to scan.")
            return
        # Disable buttons to avoid multiple scans
        self.progress['value'] = 0
        self.groups_tree.delete(*self.groups_tree.get_children())
        for widget in self.thumb_container.winfo_children():
            widget.destroy()
        self.thumbs_cache.clear()
        self.duplicate_map.clear()

        threading.Thread(target=self._run_scan, daemon=True).start()

    def _run_scan(self):
        def progress_cb(current, total):
            percent = int((current / total) * 100)
            self.progress.after(0, lambda: self.progress.configure(value=percent))

        scanner = self.scanner
        try:
            data = scanner.scan(self.selected_folders, progress_callback=progress_cb,
                                include_exts=['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'])
        except Exception as e:
            messagebox.showerror("Scan Error", str(e))
            return

        if scanner.is_cancelled():
            self.progress.after(0, lambda: self.progress.configure(value=0))
            messagebox.showinfo("Cancelled", "Scan was cancelled.")
            return

        # Filter only hashes with >1 file (duplicates)
        duplicates = {k: v for k, v in data.items() if len(v) > 1}
        self.duplicate_map = duplicates

        # Populate groups_tree
        def populate():
            self.groups_tree.delete(*self.groups_tree.get_children())
            for idx, (md5, items) in enumerate(sorted(duplicates.items(), key=lambda x: -len(x[1]))):
                node = self.groups_tree.insert('', 'end', iid=md5, values=(len(items),))
            self.progress.configure(value=100)

        self.progress.after(0, populate)

    def cancel_scan(self):
        self.scanner.cancel()

    def on_group_select(self, event):
        selected = self.groups_tree.selection()
        if not selected:
            return
        md5 = selected[0]
        group = self.duplicate_map.get(md5, [])
        self.show_group_thumbs(md5, group)

    def show_group_thumbs(self, md5: str, group: List[Dict]):
        # Clear existing
        for widget in self.thumb_container.winfo_children():
            widget.destroy()

        # For each file, show thumbnail, path, size, mtime, and a checkbox
        for i, info in enumerate(group):
            frm = ttk.Frame(self.thumb_container, relief=tk.RAISED, borderwidth=1, padding=6)
            frm.grid(row=i//2, column=i%2, padx=6, pady=6, sticky='nw')

            path = info['path']
            thumb = self.get_thumbnail(path)
            lbl = ttk.Label(frm, image=thumb)
            lbl.image = thumb
            lbl.pack()

            ttk.Label(frm, text=os.path.basename(path), wraplength=150).pack()
            size_kb = info['size'] / 1024
            dt = datetime.fromtimestamp(info['mtime']).strftime('%Y-%m-%d %H:%M:%S')
            ttk.Label(frm, text=f"{size_kb:.1f} KB | {dt}").pack()

            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(frm, text="Delete", variable=var)
            chk.var = var
            chk.pack()
            frm.delete_var = var
            frm.file_info = info

        # Add a small help label
        ttk.Label(self.thumb_container, text="Select items to delete (if Manual) or press 'Delete Selected/Policy' to act.").grid(row=999, column=0, columnspan=2, pady=8)

    def get_thumbnail(self, path: str):
        if path in self.thumbs_cache:
            return self.thumbs_cache[path]
        try:
            img = Image.open(path)
            img.thumbnail(THUMB_SIZE)
            tkimg = ImageTk.PhotoImage(img)
        except Exception:
            # Fallback: create blank image
            img = Image.new('RGB', THUMB_SIZE, color=(220,220,220))
            tkimg = ImageTk.PhotoImage(img)
        self.thumbs_cache[path] = tkimg
        return tkimg

    def choose_keep_candidate(self, group: List[Dict]) -> Tuple[Dict, List[Dict]]:
        """Return (keep_item, delete_candidates) based on policy."""
        policy = self.policy_var.get()
        if policy == 'manual':
            # In manual mode, nothing is auto-selected
            return None, group

        # derive comparator
        if policy == 'keep_newest':
            key = lambda x: x['mtime']
            reverse = True
        elif policy == 'keep_oldest':
            key = lambda x: x['mtime']
            reverse = False
        elif policy == 'keep_largest':
            key = lambda x: x['size']
            reverse = True
        elif policy == 'keep_smallest':
            key = lambda x: x['size']
            reverse = False
        else:
            key = lambda x: x['mtime']
            reverse = True

        sorted_group = sorted(group, key=key, reverse=reverse)
        keep = sorted_group[0]
        to_delete = sorted_group[1:]
        return keep, to_delete

    def delete_by_policy(self):
        if not self.duplicate_map:
            messagebox.showinfo("No duplicates", "No duplicate groups available to delete.")
            return

        manual = (self.policy_var.get() == 'manual')
        all_candidates = []
        for md5, group in self.duplicate_map.items():
            if manual:
                # collect those checked in the UI
                # traverse thumb_container children to find checked ones
                for child in self.thumb_container.winfo_children():
                    if hasattr(child, 'file_info') and hasattr(child, 'delete_var'):
                        if child.delete_var.get():
                            all_candidates.append(child.file_info['path'])
            else:
                keep, to_delete = self.choose_keep_candidate(group)
                if to_delete:
                    all_candidates.extend([it['path'] for it in to_delete])

        if not all_candidates:
            messagebox.showinfo("Nothing to delete", "No files selected or no candidates found according to policy.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Delete {len(all_candidates)} files? This cannot be undone.")
        if not confirm:
            return

        deleted = 0
        errors = []
        for p in all_candidates:
            try:
                os.remove(p)
                deleted += 1
            except Exception as e:
                errors.append((p, str(e)))

        # Refresh: remove deleted files from duplicate_map
        new_map = {}
        for md5, group in self.duplicate_map.items():
            remaining = [it for it in group if os.path.exists(it['path'])]
            if len(remaining) > 1:
                new_map[md5] = remaining
        self.duplicate_map = new_map

        # Update UI
        self.groups_tree.delete(*self.groups_tree.get_children())
        for md5, items in self.duplicate_map.items():
            self.groups_tree.insert('', 'end', iid=md5, values=(len(items),))

        msg = f"Deleted: {deleted} files."
        if errors:
            msg += f"\nErrors: {len(errors)} (see console)."
            print("Errors deleting files:")
            for e in errors:
                print(e)
        messagebox.showinfo("Done", msg)

    def export_report(self):
        if not self.duplicate_map:
            messagebox.showinfo("No Data", "No duplicate data to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON', '*.json')])
        if not path:
            return
        serial = {}
        for md5, items in self.duplicate_map.items():
            serial[md5] = items
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(serial, f, indent=2, default=str)
        messagebox.showinfo("Exported", f"Report saved to {path}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
