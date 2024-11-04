import tkinter as tk
from tkinter import filedialog, font
from logic import DistractionFreeEditorLogic

class DFWriter:
    def __init__(self, master):
        self.master = master
        self.master.title("Distraction-Free Typing Tool")
        self.master.configure(bg='#1e1e1e')
        
        # Remove window decorations and set fullscreen for Raspberry Pi
        self.master.attributes('-fullscreen', True)  # Full screen mode
        self.master.attributes('-type', 'dock')  # Removes window decorations
        self.master.geometry("400x1280")  # Match your screen resolution
        
        # Override window manager close button
        self.master.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        
        # Bind additional keys for safety
        self.master.bind('<Escape>', self.toggle_fullscreen)
        self.master.bind('<Control-q>', self.confirm_exit)
        self.is_fullscreen = True

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

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Return to fullscreen mode
            self.master.attributes('-fullscreen', True)
            self.master.attributes('-type', 'dock')
        else:
            # Exit fullscreen but maintain a maximized window
            self.master.attributes('-fullscreen', False)
            self.master.attributes('-type', 'normal')
            # Center the window
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 1280) // 2
            self.master.geometry(f"400x1280+{x}+{y}")

    def confirm_exit(self, event=None):
        # Create a simple confirmation dialog
        dialog = tk.Toplevel(self.master)
        dialog.attributes('-type', 'dialog')  # Make sure dialog appears above main window
        dialog.title("Confirm Exit")
        dialog.geometry("300x100")
        dialog.transient(self.master)
        
        label = tk.Label(dialog, text="Are you sure you want to exit?")
        label.pack(pady=10)
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Yes", command=self.master.quit).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="No", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        # Make dialog modal
        dialog.grab_set()
        dialog.focus_set()

    # Rest of the class methods remain the same
    def create_layout(self):
        self.main_frame = tk.Frame(self.master, bg='#1e1e1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_title_bar()
        self.create_toolbar()
        self.create_text_widget()

    def create_text_widget(self):
        self.text_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', 
                                   insertbackground='white', font=self.editor_font,
                                   padx=50, pady=10, borderwidth=0, highlightthickness=0)
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.text_widget.bind('<KeyRelease>', self.logic.update_text_color)

        # Configure tags for different brightness levels
        for i in range(5):
            color = self.logic.interpolate_color('#ffffff', '#4a4a4a', i/4)
            self.text_widget.tag_configure(f"color_{i}", foreground=color)

    def create_title_bar(self):
        self.title_bar = tk.Frame(self.main_frame, bg='#282c34', height=30)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.title_bar.pack_propagate(False)

        # Add fullscreen toggle button
        self.fullscreen_btn = tk.Button(self.title_bar, text="⛶", command=self.toggle_fullscreen,
                                      bg='#282c34', fg='white', bd=0, font=self.button_font)
        self.fullscreen_btn.pack(side=tk.RIGHT, padx=5)

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

        self.update_breadcrumb("My Story", "Chapter 1", 1)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.main_frame, bg='#282c34', height=30)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar.pack_propagate(False)

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
 