import tkinter
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter.messagebox import *
from tkinter.filedialog import *


class Notepad:
    __root = Tk()

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):
        # Set icon
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        # Set window size (the default is 300x300)
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Untitled - Advanced Notepad")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-alling
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-allign
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' %
                             (self.__thisWidth, self.__thisHeight, left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # To open new file
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # Add search menu
        self.__thisSearchMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisSearchMenu.add_command(label="Find", command=self.__showFind)
        self.__thisSearchMenu.add_command(label="Replace", command=self.__showReplace)
        self.__thisMenuBar.add_cascade(label="Search", menu=self.__thisSearchMenu)

        # Add View menu  
        self.__thisViewMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisViewMenu.add_command(label="Word Count", command=self.__showWordCount)
        self.__thisViewMenu.add_command(label="Select Font", command=self.__selectFont)
        self.__thisMenuBar.add_cascade(label="View", menu=self.__thisViewMenu)

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    # exit()

    def __showAbout(self):
        showinfo("Advanced Notepad", "A feature-rich text editor built with Python and Tkinter.\n\nFeatures: Search, Replace, Word Count, Font Selection")

    def __openFile(self):

        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents",
                                                        "*.txt")])

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")

        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def __showFind(self):
        """Show find dialog"""
        find_dialog = Toplevel(self.__root)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")
        find_dialog.resizable(False, False)

        Label(find_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        find_entry = Entry(find_dialog, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        find_entry.focus_set()

        def do_find():
            search_term = find_entry.get()
            if search_term:
                # Remove previous tags
                self.__thisTextArea.tag_remove("search", "1.0", END)
                # Search and highlight
                idx = "1.0"
                while True:
                    idx = self.__thisTextArea.search(search_term, idx, nocase=True, stopindex=END)
                    if not idx:
                        break
                    end_idx = f"{idx}+{len(search_term)}c"
                    self.__thisTextArea.tag_add("search", idx, end_idx)
                    idx = end_idx
                self.__thisTextArea.tag_config("search", background="yellow", foreground="black")

        Button(find_dialog, text="Find All", command=do_find).grid(row=1, column=1, pady=10, sticky="e")

    def __showReplace(self):
        """Show find and replace dialog"""
        replace_dialog = Toplevel(self.__root)
        replace_dialog.title("Find and Replace")
        replace_dialog.geometry("350x150")
        replace_dialog.resizable(False, False)

        Label(replace_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        find_entry = Entry(replace_dialog, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        find_entry.focus_set()

        Label(replace_dialog, text="Replace with:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        replace_entry = Entry(replace_dialog, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        def do_replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                content = self.__thisTextArea.get("1.0", END)
                new_content = content.replace(find_text, replace_text)
                self.__thisTextArea.delete("1.0", END)
                self.__thisTextArea.insert("1.0", new_content)

        Button(replace_dialog, text="Replace All", command=do_replace_all).grid(row=2, column=1, pady=10, sticky="e")

    def __showWordCount(self):
        """Show word count statistics"""
        content = self.__thisTextArea.get("1.0", END)
        chars = len(content) - 1  # Subtract trailing newline
        words = len(content.split())
        lines = content.count('\n')
        showinfo("Word Count", f"Characters: {chars}\nWords: {words}\nLines: {lines}")

    def __selectFont(self):
        """Allow user to select font"""
        font_dialog = Toplevel(self.__root)
        font_dialog.title("Select Font")
        font_dialog.geometry("300x200")
        font_dialog.resizable(False, False)

        Label(font_dialog, text="Font Family:").pack(pady=5)
        font_var = StringVar(value="Courier")
        font_list = ["Courier", "Arial", "Times New Roman", "Helvetica", "Verdana"]
        font_menu = ttk.Combobox(font_dialog, textvariable=font_var, values=font_list, state="readonly")
        font_menu.pack(pady=5)

        Label(font_dialog, text="Font Size:").pack(pady=5)
        size_var = IntVar(value=12)
        size_spin = Spinbox(font_dialog, from_=8, to=72, textvariable=size_var, width=10)
        size_spin.pack(pady=5)

        def apply_font():
            self.__thisTextArea.config(font=(font_var.get(), size_var.get()))
            font_dialog.destroy()

        Button(font_dialog, text="Apply", command=apply_font).pack(pady=10)

    def run(self):

        # Run main application
        self.__root.mainloop()

    # Run main application


notepad = Notepad(width=600, height=400)
notepad.run()
