import tkinter as tk
from tkinter import ttk
import os
from file_operations import FileManager

class BookNavigator(tk.Toplevel):
    """Book-focused navigation dialog - shows books, chapters, and pages"""
    def __init__(self, parent, mode='open', title="Navigate Book", current_book_path=None):
        super().__init__(parent)
        self.result = None
        self.mode = mode  # 'open' or 'navigate'
        self.file_manager = FileManager()
        self.current_book_path = current_book_path  # If provided, skip book selection
        
        # Configure dialog to match app's wide-screen design
        self.configure(bg='#1e1e1e')
        self.title(title)
        
        # Get parent window dimensions for wide-screen layout
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 1280
        parent_height = parent.winfo_height() if parent.winfo_height() > 1 else 400
        
        # Use wide-screen dimensions
        dialog_width = min(1200, parent_width - 80)
        dialog_height = min(600, parent_height - 80)
        
        # Center on parent
        x = parent.winfo_x() + (parent_width - dialog_width) // 2
        y = parent.winfo_y() + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.transient(parent)
        self.grab_set()
        self.attributes('-topmost', True)
        
        self.selected_book_path = None
        self.selected_chapter = None
        self.selected_page = None
        
        self.create_widgets()
        
        # If we have a current book, skip book selection and load chapters directly
        if self.current_book_path:
            self.selected_book_path = self.current_book_path
            # Hide books column (it was never packed, so just ensure it's not visible)
            self.books_frame.pack_forget()
            # Load chapters for current book
            self.load_chapters(self.current_book_path)
            # Auto-select first chapter if available
            if self.chapters_listbox.size() > 0:
                self.chapters_listbox.selection_set(0)
                self.on_chapter_select()
        else:
            # Show books column and load all books
            self.books_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
            self.load_books()
        
        # Keyboard navigation
        self.bind('<Return>', lambda e: self.confirm())
        self.bind('<Escape>', lambda e: self.cancel())
        self.bind('<Right>', lambda e: self.navigate_horizontal(1))
        self.bind('<Left>', lambda e: self.navigate_horizontal(-1))
        self.bind('<Up>', lambda e: self.navigate_vertical(-1))
        self.bind('<Down>', lambda e: self.navigate_vertical(1))
        
        # Focus for keyboard - use after to ensure dialog is fully created
        self.after(50, self.setup_focus)
    
    def setup_focus(self):
        """Set focus on dialog for keyboard navigation"""
        self.focus_set()
        # Focus on appropriate listbox based on current state
        if self.current_book_path:
            # If we're in a book, focus on chapters
            if hasattr(self, 'chapters_listbox') and self.chapters_listbox.winfo_exists():
                self.chapters_listbox.focus_set()
        else:
            # Otherwise focus on books
            if hasattr(self, 'books_listbox') and self.books_listbox.winfo_exists():
                self.books_listbox.focus_set()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg='#282c34', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=self.title(), font=("Arial", 14, "bold"),
                bg='#282c34', fg='white').pack(pady=15)
        
        # Main content area with three columns
        content = tk.Frame(self, bg='#1e1e1e')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Books column (only shown if no current_book_path)
        self.books_frame = tk.Frame(content, bg='#1e1e1e', width=300)
        # Will be packed or hidden based on current_book_path
        
        tk.Label(self.books_frame, text="Books", font=("Arial", 11, "bold"),
                bg='#1e1e1e', fg='white').pack(anchor=tk.W, pady=(0, 10))
        
        books_list_frame = tk.Frame(self.books_frame, bg='#1e1e1e')
        books_list_frame.pack(fill=tk.BOTH, expand=True)
        
        books_scrollbar = tk.Scrollbar(books_list_frame)
        books_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.books_listbox = tk.Listbox(books_list_frame,
                                       bg='#282c34', fg='white',
                                       selectbackground='#4e5563',
                                       font=("Arial", 10),
                                       yscrollcommand=books_scrollbar.set,
                                       borderwidth=0, highlightthickness=0)
        self.books_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        books_scrollbar.config(command=self.books_listbox.yview)
        
        self.books_listbox.bind('<<ListboxSelect>>', self.on_book_select)
        self.books_listbox.bind('<Double-Button-1>', lambda e: self.on_book_select(e) or self.confirm())
        
        # Chapters column
        chapters_frame = tk.Frame(content, bg='#1e1e1e', width=300)
        chapters_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        chapters_frame.pack_propagate(False)
        
        tk.Label(chapters_frame, text="Chapters", font=("Arial", 11, "bold"),
                bg='#1e1e1e', fg='white').pack(anchor=tk.W, pady=(0, 10))
        
        chapters_list_frame = tk.Frame(chapters_frame, bg='#1e1e1e')
        chapters_list_frame.pack(fill=tk.BOTH, expand=True)
        
        chapters_scrollbar = tk.Scrollbar(chapters_list_frame)
        chapters_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chapters_listbox = tk.Listbox(chapters_list_frame,
                                          bg='#282c34', fg='white',
                                          selectbackground='#4e5563',
                                          font=("Arial", 10),
                                          yscrollcommand=chapters_scrollbar.set,
                                          borderwidth=0, highlightthickness=0)
        self.chapters_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chapters_scrollbar.config(command=self.chapters_listbox.yview)
        
        self.chapters_listbox.bind('<<ListboxSelect>>', self.on_chapter_select)
        self.chapters_listbox.bind('<Double-Button-1>', lambda e: self.on_chapter_select(e) or self.confirm())
        
        # Pages column
        pages_frame = tk.Frame(content, bg='#1e1e1e', width=300)
        pages_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pages_frame.pack_propagate(False)
        
        tk.Label(pages_frame, text="Pages", font=("Arial", 11, "bold"),
                bg='#1e1e1e', fg='white').pack(anchor=tk.W, pady=(0, 10))
        
        pages_list_frame = tk.Frame(pages_frame, bg='#1e1e1e')
        pages_list_frame.pack(fill=tk.BOTH, expand=True)
        
        pages_scrollbar = tk.Scrollbar(pages_list_frame)
        pages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pages_listbox = tk.Listbox(pages_list_frame,
                                       bg='#282c34', fg='white',
                                       selectbackground='#4e5563',
                                       font=("Arial", 10),
                                       yscrollcommand=pages_scrollbar.set,
                                       borderwidth=0, highlightthickness=0)
        self.pages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pages_scrollbar.config(command=self.pages_listbox.yview)
        
        self.pages_listbox.bind('<<ListboxSelect>>', self.on_page_select)
        self.pages_listbox.bind('<Double-Button-1>', lambda e: self.on_page_select(e) or self.confirm())
        
        # Buttons
        button_frame = tk.Frame(self, bg='#1e1e1e', height=60)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel,
                             bg='#3e4451', fg='white', font=("Arial", 10),
                             padx=20, pady=5, bd=0, activebackground='#4a5567')
        cancel_btn.pack(side=tk.RIGHT, padx=10, pady=15)
        
        confirm_text = "Open" if self.mode == 'open' else "Select"
        self.confirm_btn = tk.Button(button_frame, text=confirm_text, command=self.confirm,
                                    bg='#3e4451', fg='white', font=("Arial", 10),
                                    padx=20, pady=5, bd=0, activebackground='#4a5567',
                                    state=tk.DISABLED)
        self.confirm_btn.pack(side=tk.RIGHT, padx=10, pady=15)
    
    def load_books(self):
        """Load all books from the file manager"""
        self.books_listbox.delete(0, tk.END)
        self.books_data = []
        
        book_dirs = self.file_manager.list_books()
        for book_dir in book_dirs:
            book_path = os.path.join(self.file_manager.base_path, book_dir)
            metadata = self.file_manager.get_metadata(book_path)
            
            if metadata:
                display_text = metadata.get("title", book_dir)
                genre = metadata.get("genre", "")
                if genre:
                    display_text += f" ({genre})"
            else:
                display_text = book_dir
            
            self.books_data.append((book_dir, book_path))
            self.books_listbox.insert(tk.END, display_text)
    
    def on_book_select(self, event=None):
        """Handle book selection"""
        selection = self.books_listbox.curselection()
        if selection:
            index = selection[0]
            book_dir, book_path = self.books_data[index]
            self.selected_book_path = book_path
            
            # Clear pages first
            self.pages_listbox.delete(0, tk.END)
            self.selected_chapter = None
            self.selected_page = None
            
            # Load chapters for this book (this will clear and populate chapters listbox)
            self.load_chapters(book_path)
            
            self.update_confirm_button()
    
    def load_chapters(self, book_path):
        """Load chapters for the selected book"""
        self.chapters_listbox.delete(0, tk.END)
        chapters = self.file_manager.list_chapters(book_path)
        
        print(f"Loading chapters for {book_path}: {chapters}")  # Debug
        
        if not chapters:
            print(f"No chapters found in {book_path}")  # Debug
            return
        
        for chapter in chapters:
            # Format chapter name nicely - replace underscores with spaces
            display_name = chapter.replace("_", " ")
            
            # If it's a numbered chapter (Chapter_01), format it nicely
            if display_name.startswith("Chapter ") and len(display_name.split()) > 1:
                try:
                    num = int(display_name.split()[1])
                    display_name = f"Chapter {num}"
                except (ValueError, IndexError):
                    # Keep original name if it doesn't match pattern
                    pass
            
            self.chapters_listbox.insert(tk.END, display_name)
            print(f"Inserted chapter: {display_name}")  # Debug
    
    def on_chapter_select(self, event=None):
        """Handle chapter selection"""
        selection = self.chapters_listbox.curselection()
        if selection and self.selected_book_path:
            index = selection[0]
            chapters = self.file_manager.list_chapters(self.selected_book_path)
            if index < len(chapters):
                self.selected_chapter = chapters[index]
                
                # Load pages for this chapter (load_pages already clears the listbox)
                self.load_pages(self.selected_book_path, self.selected_chapter)
                self.selected_page = None  # Reset page selection
                self.update_confirm_button()
    
    def load_pages(self, book_path, chapter_name):
        """Load pages for the selected chapter"""
        self.pages_listbox.delete(0, tk.END)
        pages = self.file_manager.list_pages(book_path, chapter_name)
        
        for page_num in pages:
            self.pages_listbox.insert(tk.END, f"Page {page_num}")
    
    def on_page_select(self, event=None):
        """Handle page selection"""
        selection = self.pages_listbox.curselection()
        if selection:
            index = selection[0]
            pages = self.file_manager.list_pages(self.selected_book_path, self.selected_chapter)
            if index < len(pages):
                self.selected_page = pages[index]
                self.update_confirm_button()
    
    def update_confirm_button(self):
        """Update confirm button state based on selection"""
        if self.selected_book_path and self.selected_chapter and self.selected_page:
            self.confirm_btn.config(state=tk.NORMAL)
        else:
            self.confirm_btn.config(state=tk.DISABLED)
    
    def confirm(self):
        """Confirm selection"""
        if self.selected_book_path and self.selected_chapter and self.selected_page:
            self.result = {
                'book_path': self.selected_book_path,
                'chapter': self.selected_chapter,
                'page': self.selected_page
            }
            self.destroy()
    
    def navigate_horizontal(self, direction):
        """Navigate between columns (Books -> Chapters -> Pages)"""
        if direction > 0:  # Right
            if self.selected_book_path and not self.selected_chapter:
                # Move from books to chapters
                if self.chapters_listbox.size() > 0:
                    self.chapters_listbox.selection_set(0)
                    self.on_chapter_select()
            elif self.selected_chapter and not self.selected_page:
                # Move from chapters to pages
                if self.pages_listbox.size() > 0:
                    self.pages_listbox.selection_set(0)
                    self.on_page_select()
        else:  # Left
            if self.selected_page:
                # Clear page selection
                self.pages_listbox.selection_clear(0, tk.END)
                self.selected_page = None
                self.update_confirm_button()
            elif self.selected_chapter:
                # Clear chapter selection
                self.chapters_listbox.selection_clear(0, tk.END)
                self.selected_chapter = None
                self.pages_listbox.delete(0, tk.END)
                self.update_confirm_button()
    
    def navigate_vertical(self, direction):
        """Navigate within current column"""
        # Only navigate in books if books column is visible
        if not self.current_book_path and self.books_listbox.curselection():
            # Navigating in books
            current = self.books_listbox.curselection()[0]
            new_index = max(0, min(current + direction, self.books_listbox.size() - 1))
            self.books_listbox.selection_clear(0, tk.END)
            self.books_listbox.selection_set(new_index)
            self.books_listbox.see(new_index)
            self.on_book_select()
        elif self.chapters_listbox.curselection():
            # Navigating in chapters
            current = self.chapters_listbox.curselection()[0]
            new_index = max(0, min(current + direction, self.chapters_listbox.size() - 1))
            self.chapters_listbox.selection_clear(0, tk.END)
            self.chapters_listbox.selection_set(new_index)
            self.chapters_listbox.see(new_index)
            self.on_chapter_select()
        elif self.pages_listbox.curselection():
            # Navigating in pages
            current = self.pages_listbox.curselection()[0]
            new_index = max(0, min(current + direction, self.pages_listbox.size() - 1))
            self.pages_listbox.selection_clear(0, tk.END)
            self.pages_listbox.selection_set(new_index)
            self.pages_listbox.see(new_index)
            self.on_page_select()
        elif self.current_book_path and not self.chapters_listbox.curselection() and self.chapters_listbox.size() > 0:
            # If in a book and no chapter selected, select first chapter
            self.chapters_listbox.selection_set(0)
            self.on_chapter_select()
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.destroy()
    
    @staticmethod
    def show(parent, mode='open', current_book_path=None):
        """Show the book navigator dialog"""
        dialog = BookNavigator(parent, mode=mode, current_book_path=current_book_path)
        parent.wait_window(dialog)
        return dialog.result

