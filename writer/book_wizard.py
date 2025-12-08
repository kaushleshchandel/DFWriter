import tkinter as tk
from tkinter import ttk, messagebox

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
        self.container = tk.Frame(self, padx=20, pady=20)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self, padx=20, pady=10)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.back_btn = tk.Button(self.button_frame, text="Back", command=self.go_back)
        self.back_btn.pack(side=tk.LEFT)
        
        self.next_btn = tk.Button(self.button_frame, text="Next", command=self.go_next)
        self.next_btn.pack(side=tk.RIGHT)

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
        tk.Label(self.container, text="Book Basics", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        tk.Label(self.container, text="Title:").pack(anchor=tk.W)
        tk.Entry(self.container, textvariable=self.book_data["title"]).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.container, text="Genre:").pack(anchor=tk.W)
        genres = ["Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "Thriller", "Romance", "Horror", "Biography", "Other"]
        ttk.Combobox(self.container, textvariable=self.book_data["genre"], values=genres).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.container, text="Description:").pack(anchor=tk.W)
        # Handle Text widget binding manually since it doesn't support textvariable
        self.desc_text = tk.Text(self.container, height=5)
        self.desc_text.pack(fill=tk.X, pady=(0, 10))
        self.desc_text.insert("1.0", self.book_data["description"].get())
        
        # Save description when leaving this step
        self.current_desc_widget = self.desc_text

    def step_goals(self):
        tk.Label(self.container, text="Writing Goals", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        tk.Label(self.container, text="Target Word Count:").pack(anchor=tk.W)
        tk.Entry(self.container, textvariable=self.book_data["target_word_count"]).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.container, text="Daily Word Goal:").pack(anchor=tk.W)
        tk.Entry(self.container, textvariable=self.book_data["daily_word_goal"]).pack(fill=tk.X, pady=(0, 10))

    def step_summary(self):
        title = self.book_data["title"].get()
        genre = self.book_data["genre"].get()
        words = self.book_data["target_word_count"].get()
        
        tk.Label(self.container, text="Ready to Start?", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        summary = f"Title: {title}\nGenre: {genre}\nTarget: {words} words"
        tk.Label(self.container, text=summary, justify=tk.LEFT).pack(anchor=tk.W)

    def go_next(self):
        # Validate and Save current step data
        if self.current_step == 0:
            if not self.book_data["title"].get().strip():
                messagebox.showerror("Error", "Title is required")
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
