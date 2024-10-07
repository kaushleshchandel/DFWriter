import tkinter as tk
from tkinter import font
from file_operations import open_file, save_file

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Text Editor")
        self.root.geometry("1280x400")

        self.setup_text_area()
        self.setup_menu()
        self.setup_toolbar()

    def setup_text_area(self):
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

    def setup_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)

    def setup_toolbar(self):
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="top", fill="x")

        self.bold_button = tk.Button(self.toolbar, text="B", width=2, command=self.toggle_bold)
        self.bold_button.pack(side="left", padx=2, pady=2)

        self.italic_button = tk.Button(self.toolbar, text="I", width=2, command=self.toggle_italic)
        self.italic_button.pack(side="left", padx=2, pady=2)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        content = open_file()
        if content:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)

    def save_file(self):
        content = self.text_area.get(1.0, tk.END)
        save_file(content)

    def toggle_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
        self.text_area.tag_configure("bold", font=font.Font(weight="bold"))

    def toggle_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
        self.text_area.tag_configure("italic", font=font.Font(slant="italic"))