import tkinter as tk
from tkinter import filedialog, font
from logic import DistractionFreeEditorLogic

class DFWriter:
    def __init__(self, master):
        self.master = master
        self.master.title("Distraction-Free Typing Tool")
        self.master.geometry("1280x400")
        self.master.configure(bg='#1e1e1e')

        self.font_size = 16
        self.editor_font = font.Font(family="Courier", size=self.font_size)

        self.logic = DistractionFreeEditorLogic(self)

        self.create_text_widget()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg='#282c34', fg='white')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.logic.new_file)
        file_menu.add_command(label="Open", command=self.logic.open_file)
        file_menu.add_command(label="Save", command=self.logic.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.logic.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        book_menu = tk.Menu(menubar, tearoff=0, bg='#282c34', fg='white')
        menubar.add_cascade(label="Book", menu=book_menu)
        book_menu.add_command(label="New", command=self.logic.new_file)
        book_menu.add_command(label="Close", command=self.logic.new_file)
        book_menu.add_command(label="Check", command=self.logic.new_file)

        editor_menu = tk.Menu(menubar, tearoff=0, bg='#282c34', fg='white')
        menubar.add_cascade(label="Editor", menu=editor_menu)
        editor_menu.add_command(label="New", command=self.logic.new_file)

        tools_menu = tk.Menu(menubar, tearoff=0, bg='#282c34', fg='white')
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="New", command=self.logic.new_file)


    def create_text_widget(self):
        self.text_widget = tk.Text(self.master, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', 
                                   insertbackground='white', font=self.editor_font,
                                   padx=50, pady=50, borderwidth=0, highlightthickness=0)
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.text_widget.bind('<KeyRelease>', self.logic.update_text_color)

        # Configure tags for different brightness levels
        for i in range(5):
            color = self.logic.interpolate_color('#ffffff', '#4a4a4a', i/4)
            self.text_widget.tag_configure(f"color_{i}", foreground=color)
 