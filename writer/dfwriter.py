import tkinter as tk
from tkinter import filedialog, font
from logic import DistractionFreeEditorLogic
import sys
import platform

class DFWriter(tk.Frame):
    def __init__(self, parent, project_path=None):
        super().__init__(parent)
        self.project_path = project_path
        self.configure(bg='#1e1e1e')
        
        # NOTE: Window setup (geometry, title) is now handled by the main App controller
        # Key bindings should be bound to the parent/root or specific widgets
        
        # Bind keyboard shortcuts
        self.master.bind('<Escape>', self.toggle_fullscreen)
        self.master.bind('<Control-q>', self.close_book)
        self.master.bind('<Control-s>', lambda e: self.logic.save_file())
        self.master.bind('<Control-o>', lambda e: self.logic.open_file())
        self.master.bind('<Control-b>', lambda e: self.logic.start_new_book_wizard())
        self.is_fullscreen = False  # Track fullscreen state

        self.font_size = 16
        self.editor_font = font.Font(family="Courier", size=self.font_size)
        self.button_font = font.Font(family="Segoe UI Symbol", size=10)
        self.title_font = font.Font(family="Arial", size=10)
        self.info_font = font.Font(family="Arial", size=9)

        # Create StringVar instances as class attributes BEFORE logic init
        self.breadcrumb_var = tk.StringVar()
        self.pages_var = tk.StringVar(value="Pages: 0")
        self.words_var = tk.StringVar(value="Words: 0")
        self.custom_var = tk.StringVar(value="Custom: 0")

        # Initialize Logic AFTER variables (so update_breadcrumb works) but BEFORE layout (so buttons work)
        self.logic = DistractionFreeEditorLogic(self, self.project_path)

        self.create_layout()
        
        # Load page content after UI is fully created
        if self.project_path:
            self.logic.load_current_page()


    def setup_window(self):
        """Configure window attributes based on platform"""
        system = platform.system().lower()
        
        if system == 'linux':
            # Linux-specific setup
            try:
                self.master.attributes('-type', 'dock')
            except tk.TclError:
                # Fallback if -type is not supported
                self.master.attributes('-zoomed', True)
        elif system == 'windows':
            # Windows-specific setup
            self.master.overrideredirect(True)  # Remove window decorations
        elif system == 'darwin':
            # macOS-specific setup
            self.master.attributes('-fullscreen', True)
        
        # Set initial window size
        self.master.geometry(f"{self.window_width}x{self.window_height}")
        
        # Center the window
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.master.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        system = platform.system().lower()

        if self.is_fullscreen:
            # Enter fullscreen mode
            if system == 'linux':
                try:
                    self.master.attributes('-type', 'dock')
                except tk.TclError:
                    self.master.attributes('-zoomed', True)
            elif system == 'windows':
                self.master.overrideredirect(True)
                self.master.state('zoomed')
            elif system == 'darwin':
                self.master.attributes('-fullscreen', True)
        else:
            # Exit fullscreen mode
            if system == 'linux':
                try:
                    self.master.attributes('-type', 'normal')
                except tk.TclError:
                    self.master.attributes('-zoomed', False)
            elif system == 'windows':
                self.master.overrideredirect(True)
                self.master.state('normal')
            elif system == 'darwin':
                self.master.attributes('-fullscreen', False)
            
            # Return to centered window
            self.center_window()

    def close_book(self, event=None):
        """Close the current book and return to book selection"""
        from wide_dialogs import WideScreenMessageDialog
        # Store reference to app before dialog (in case self gets destroyed)
        app = self.master
        
        print(f"DEBUG: close_book called, app type: {type(app)}, has show_project_picker: {hasattr(app, 'show_project_picker')}")
        
        result = WideScreenMessageDialog.askyesno(
            app,
            title="Close Book",
            message="Are you sure you want to close this book?"
        )
        
        print(f"DEBUG: Dialog returned: {result}")
        
        # After dialog closes (wait_window completes), switch to project picker
        if result:
            print("DEBUG: About to call show_project_picker")
            try:
                # Use after to ensure we're back in the main event loop after wait_window
                def do_switch():
                    print("DEBUG: Inside do_switch callback")
                    if hasattr(app, 'show_project_picker'):
                        print("DEBUG: Calling show_project_picker")
                        app.show_project_picker()
                        print("DEBUG: show_project_picker called")
                    else:
                        print("ERROR: app does not have show_project_picker method")
                app.after(50, do_switch)
            except Exception as e:
                print(f"ERROR: Exception in close_book: {e}")
                import traceback
                traceback.print_exc()

    def create_layout(self):
        self.main_frame = tk.Frame(self.master, bg='#1e1e1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_title_bar()
        self.create_toolbar()
        self.create_text_widget()

    def create_text_widget(self):
        self.text_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        # Create text widget with generous padding for a comfortable writing experience
        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, bg='#1e1e1e', fg='#ffffff', 
                                   insertbackground='white', font=self.editor_font,
                                   padx=100, pady=20, borderwidth=0, highlightthickness=0)
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

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.main_frame, bg='#282c34', height=30)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar.pack_propagate(False)

        buttons = [
            ("📖 New Book (Ctrl+B)", self.logic.start_new_book_wizard),
            ("📂 Open Page (Ctrl+O)", self.logic.open_file),
            ("💾 Save (Ctrl+S)", self.logic.save_file),
            ("📄 New Page", self.logic.new_page),
            ("📑 New Chapter", self.logic.new_chapter),
            ("📕 Close Book (Ctrl+Q)", self.close_book)
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