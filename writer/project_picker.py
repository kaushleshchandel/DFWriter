import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from file_operations import FileManager
from book_wizard import BookWizard

class ProjectPicker(tk.Frame):
    def __init__(self, parent, on_project_selected):
        super().__init__(parent)
        self.configure(bg='#1e1e1e')
        
        self.on_project_selected = on_project_selected
        self.file_manager = FileManager()
        
        self.create_widgets()
        self.load_projects()

    # center_window removed as it is handled by the main app window

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg='#282c34', pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Select a Project", font=("Arial", 16, "bold"), 
                 bg='#282c34', fg='white').pack()

        # Main Content
        content_frame = tk.Frame(self, bg='#1e1e1e', padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox with Scrollbar
        list_frame = tk.Frame(content_frame, bg='#1e1e1e')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.project_list = tk.Listbox(list_frame, font=("Arial", 12), 
                                     bg='#282c34', fg='white', selectbackground='#4e5563',
                                     yscrollcommand=scrollbar.set, borderwidth=0, highlightthickness=0)
        self.project_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.project_list.yview)
        
        self.project_list.bind('<<ListboxSelect>>', self.on_select)
        self.project_list.bind('<Double-Button-1>', self.open_selected)

        # Buttons
        button_frame = tk.Frame(self, bg='#1e1e1e', pady=20)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Button(button_frame, text="New Book", command=self.start_new_book,
                 bg='#3e4451', fg='white', font=("Segoe UI", 10), padx=15, pady=5, bd=0).pack(side=tk.LEFT, padx=20)
        
        self.open_btn = tk.Button(button_frame, text="Open Selected", command=self.open_selected,
                 bg='#3e4451', fg='white', font=("Segoe UI", 10), padx=15, pady=5, bd=0, state=tk.DISABLED)
        self.open_btn.pack(side=tk.RIGHT, padx=20)

    def load_projects(self):
        self.project_list.delete(0, tk.END)
        self.projects = []
        
        book_dirs = self.file_manager.list_books()
        print(f"Found book directories: {book_dirs}") # Debug
        
        for book_dir in book_dirs:
            book_path = os.path.join(self.file_manager.base_path, book_dir)
            metadata_path = os.path.join(book_path, "metadata.json")
            
            display_text = book_dir
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        title = metadata.get("title", book_dir)
                        genre = metadata.get("genre", "Unknown")
                        display_text = f"{title} ({genre})"
                except Exception as e:
                    print(f"Error loading metadata for {book_dir}: {e}")
            
            self.projects.append(book_path)
            self.project_list.insert(tk.END, display_text)

    def on_select(self, event):
        selection = self.project_list.curselection()
        if selection:
            self.open_btn.config(state=tk.NORMAL)
        else:
            self.open_btn.config(state=tk.DISABLED)

    def start_new_book(self):
        self.master.show_book_wizard()

    # on_book_created removed (logic moved to DFWriterApp)

    def open_selected(self, event=None):
        selection = self.project_list.curselection()
        if selection:
            index = selection[0]
            # Since we display "Title (Genre)", we need to lookup using the parallel list self.projects
            project_path = self.projects[index]
            self.on_project_selected(project_path)
