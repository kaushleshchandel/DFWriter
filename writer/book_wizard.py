import tkinter as tk
from tkinter import ttk, messagebox
from wide_dialogs import WideScreenMessageDialog

class BookWizard(tk.Frame):
    def __init__(self, parent, on_complete):
        super().__init__(parent)
        self.configure(bg='#1e1e1e')
        
        self.on_complete = on_complete
        self.current_step = 0
        self.steps = [self.step_basics, self.step_goals, self.step_summary]
        
        # Data storage
        self.book_data = {
            "title": tk.StringVar(),
            "genre": tk.StringVar(),
            "description": tk.StringVar(),
            "target_word_count": tk.StringVar(value="50000"),
            "daily_word_goal": tk.StringVar(value="1000")
        }
        
        self.create_widgets()
        self.show_step(0)

    def create_widgets(self):
        # Use wide-screen layout with centered content
        # Main container that fills the frame
        main_container = tk.Frame(self, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Button frame at the bottom (fixed height, always visible)
        self.button_frame = tk.Frame(main_container, bg='#1e1e1e', height=70)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.button_frame.pack_propagate(False)
        
        # Content area above buttons (takes remaining space)
        content_wrapper = tk.Frame(main_container, bg='#1e1e1e')
        content_wrapper.pack(fill=tk.BOTH, expand=True, padx=100, pady=40)
        
        self.container = tk.Frame(content_wrapper, bg='#1e1e1e')
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons in the button frame
        self.back_btn = tk.Button(self.button_frame, text="Back", command=self.go_back,
                                  bg='#3e4451', fg='white', font=("Arial", 11),
                                  padx=25, pady=8, bd=0, activebackground='#4a5567',
                                  cursor='hand2')
        self.back_btn.pack(side=tk.LEFT, padx=30, pady=15)
        
        self.next_btn = tk.Button(self.button_frame, text="Next", command=self.go_next,
                                 bg='#3e4451', fg='white', font=("Arial", 11),
                                 padx=25, pady=8, bd=0, activebackground='#4a5567',
                                 cursor='hand2')
        self.next_btn.pack(side=tk.RIGHT, padx=30, pady=15)
        
        # Bind keyboard shortcuts
        self.bind('<Return>', lambda e: self.go_next())
        self.bind('<Escape>', lambda e: self.go_back() if self.current_step > 0 else None)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_step(self, step_index):
        self.clear_container()
        self.steps[step_index]()
        
        # Update buttons
        self.back_btn.config(state=tk.NORMAL if step_index > 0 else tk.DISABLED)
        self.next_btn.config(text="Finish" if step_index == len(self.steps) - 1 else "Next")

    def step_basics(self):
        tk.Label(self.container, text="Book Basics", font=("Arial", 18, "bold"),
                bg='#1e1e1e', fg='white').pack(pady=(0, 30))
        
        # Title field
        title_frame = tk.Frame(self.container, bg='#1e1e1e')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(title_frame, text="Title:", bg='#1e1e1e', fg='white',
                font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        title_entry = tk.Entry(title_frame, textvariable=self.book_data["title"],
                              bg='#282c34', fg='white', insertbackground='white',
                              font=("Arial", 11), borderwidth=1, relief=tk.SOLID)
        title_entry.pack(fill=tk.X)
        
        # Genre field
        genre_frame = tk.Frame(self.container, bg='#1e1e1e')
        genre_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(genre_frame, text="Genre:", bg='#1e1e1e', fg='white',
                font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        genres = ["Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "Thriller", "Romance", "Horror", "Biography", "Other"]
        genre_combo = ttk.Combobox(genre_frame, textvariable=self.book_data["genre"],
                                   values=genres, font=("Arial", 11), state='readonly')
        genre_combo.pack(fill=tk.X)
        
        # Description field
        desc_frame = tk.Frame(self.container, bg='#1e1e1e')
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        tk.Label(desc_frame, text="Description:", bg='#1e1e1e', fg='white',
                font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        self.desc_text = tk.Text(desc_frame, height=8, bg='#282c34', fg='white',
                                 insertbackground='white', font=("Arial", 10),
                                 borderwidth=1, relief=tk.SOLID, wrap=tk.WORD)
        self.desc_text.pack(fill=tk.BOTH, expand=True)
        self.desc_text.insert("1.0", self.book_data["description"].get())
        
        self.current_desc_widget = self.desc_text

    def step_goals(self):
        tk.Label(self.container, text="Writing Goals", font=("Arial", 18, "bold"),
                bg='#1e1e1e', fg='white').pack(pady=(0, 40))
        
        # Target word count
        target_frame = tk.Frame(self.container, bg='#1e1e1e')
        target_frame.pack(fill=tk.X, pady=(0, 30))
        tk.Label(target_frame, text="Target Word Count:", bg='#1e1e1e', fg='white',
                font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        target_entry = tk.Entry(target_frame, textvariable=self.book_data["target_word_count"],
                               bg='#282c34', fg='white', insertbackground='white',
                               font=("Arial", 11), borderwidth=1, relief=tk.SOLID)
        target_entry.pack(fill=tk.X)
        
        # Daily word goal
        daily_frame = tk.Frame(self.container, bg='#1e1e1e')
        daily_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(daily_frame, text="Daily Word Goal:", bg='#1e1e1e', fg='white',
                font=("Arial", 11)).pack(anchor=tk.W, pady=(0, 5))
        daily_entry = tk.Entry(daily_frame, textvariable=self.book_data["daily_word_goal"],
                               bg='#282c34', fg='white', insertbackground='white',
                               font=("Arial", 11), borderwidth=1, relief=tk.SOLID)
        daily_entry.pack(fill=tk.X)

    def step_summary(self):
        title = self.book_data["title"].get()
        genre = self.book_data["genre"].get()
        words = self.book_data["target_word_count"].get()
        daily = self.book_data["daily_word_goal"].get()
        
        tk.Label(self.container, text="Ready to Start?", font=("Arial", 18, "bold"),
                bg='#1e1e1e', fg='white').pack(pady=(0, 40))
        
        summary_frame = tk.Frame(self.container, bg='#282c34', relief=tk.SOLID, borderwidth=1)
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        summary_text = f"Title: {title}\nGenre: {genre}\nTarget Word Count: {words}\nDaily Word Goal: {daily}"
        tk.Label(summary_frame, text=summary_text, bg='#282c34', fg='white',
                font=("Arial", 11), justify=tk.LEFT, anchor='w', padx=20, pady=20).pack(fill=tk.X)

    def go_back(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)

    def go_next(self):
        # Validate and Save current step data
        if self.current_step == 0:
            if not self.book_data["title"].get().strip():
                WideScreenMessageDialog.showerror(self.master, "Error", "Title is required")
                return
            # Save description from text widget
            if hasattr(self, 'current_desc_widget') and self.current_desc_widget.winfo_exists():
                self.book_data["description"].set(self.current_desc_widget.get("1.0", tk.END).strip())
        
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step(self.current_step)
        else:
            self.finish()

    def finish(self):
        # Prepare result dictionary
        result = {k: v.get() for k, v in self.book_data.items()}
        self.on_complete(result)
        self.destroy()
