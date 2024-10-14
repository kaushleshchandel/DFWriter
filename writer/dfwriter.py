import tkinter as tk
from tkinter import filedialog, font
from logic import DistractionFreeEditorLogic

class DFWriter:
    def __init__(self, master):
        self.master = master
        self.master.title("Distraction-Free Typing Tool")
        self.master.geometry("1024x400")
        self.master.configure(bg='#1e1e1e')
        self.master.resizable(False, False)  # Disable resizing

        self.font_size = 16
        self.editor_font = font.Font(family="Courier", size=self.font_size)
        self.button_font = font.Font(family="Segoe UI Symbol", size=10)
        self.title_font = font.Font(family="Arial", size=10)
        self.info_font = font.Font(family="Arial", size=9)

        self.logic = DistractionFreeEditorLogic(self)

        # Create StringVar instances as class attributes
        self.breadcrumb_var = tk.StringVar()
        self.pages_var = tk.StringVar(value="Pages: 0")
        self.words_var = tk.StringVar(value="Words: 0")
        self.custom_var = tk.StringVar(value="Custom: 0")

        self.create_layout()
       # self.create_menu()

    def create_layout(self):
        self.main_frame = tk.Frame(self.master, bg='#1e1e1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_title_bar()
        self.create_toolbar()
        self.create_text_widget()

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

    def create_title_bar(self):
        self.title_bar = tk.Frame(self.main_frame, bg='#282c34', height=30)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.title_bar.pack_propagate(False)

        # Breadcrumb (left-aligned)
        self.breadcrumb_label = tk.Label(self.title_bar, textvariable=self.breadcrumb_var,
                                         bg='#282c34', fg='white', font=self.title_font,
                                         padx=10, pady=5, anchor='w')
        self.breadcrumb_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Info elements (right-aligned)
        self.info_frame = tk.Frame(self.title_bar, bg='#282c34')
        self.info_frame.pack(side=tk.RIGHT, padx=10)

        info_labels = [
            (self.pages_var, "Pages"),
            (self.words_var, "Words"),
            (self.custom_var, "Custom")
        ]

        for var, name in info_labels:
            label = tk.Label(self.info_frame, textvariable=var, bg='#282c34', fg='white',
                             font=self.info_font, padx=5)
            label.pack(side=tk.LEFT)

        # Initialize with dummy data
        self.update_breadcrumb("My Story", "Chapter 1", 1)

    def create_text_widget(self):
        self.text_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        # Calculate the height for the text widget
        total_other_height = self.title_bar.winfo_reqheight() + 30  # 30 is the toolbar height
        text_height = 400 - total_other_height - 4  # 4 pixels for padding

        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', 
                                   insertbackground='white', font=self.editor_font,
                                   padx=50, pady=10, borderwidth=0, highlightthickness=0,
                                   height=int(text_height / self.editor_font.metrics()['linespace']))
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.text_widget.bind('<KeyRelease>', self.logic.update_text_color)

        # Configure tags for different brightness levels
        for i in range(5):
            color = self.logic.interpolate_color('#ffffff', '#4a4a4a', i/4)
            self.text_widget.tag_configure(f"color_{i}", foreground=color)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.main_frame, bg='#282c34', height=30)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar.pack_propagate(False)  # Ensure the toolbar maintains its height

        buttons = [
            ("+ New", self.logic.new_file),
            ("📂 Open", self.logic.open_file),
            ("💾 Save", self.logic.save_file),
            ("⚙ Settings", self.logic.save_file),
            ("❌ Exit", self.master.quit)
        ]

        for text, command in buttons:
            btn = tk.Button(self.toolbar, text=text, command=command, 
                            bg='#3e4451', fg='white',
                            activebackground='#4a5567', activeforeground='white',
                            bd=0, padx=10, pady=2, font=self.button_font)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def update_breadcrumb(self, story_title, chapter, page_number):
        breadcrumb_text = f"{story_title} > {chapter} > Page {page_number}"
        self.breadcrumb_var.set(breadcrumb_text)

    def get_story_title(self):
        return "My Story"

    def get_current_chapter(self):
        return "Chapter 1"

    def get_current_page(self):
        return 1

    def update_title_bar(self):
        story_title = self.get_story_title()
        chapter = self.get_current_chapter()
        page = self.get_current_page()
        self.update_breadcrumb(story_title, chapter, page)

    def update_pages(self, pages):
        self.pages_var.set(f"Pages: {pages}")

    def update_words(self, words):
        self.words_var.set(f"Words: {words}")

    def update_custom(self, value, label="Custom"):
        self.custom_var.set(f"{label}: {value}")
 