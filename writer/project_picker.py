import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from file_operations import FileManager
from book_wizard import BookWizard
from book_card import BookCard
from new_book_card import NewBookCard

class ProjectPicker(tk.Frame):
    def __init__(self, parent, on_project_selected):
        super().__init__(parent)
        self.configure(bg='#1e1e1e')
        
        self.on_project_selected = on_project_selected
        self.file_manager = FileManager()
        self.selected_index = -1
        self.book_cards = []
        self.book_paths = []
        
        self.create_widgets()
        self.load_projects()
        
        # Focus for keyboard navigation - set after a short delay to ensure widgets are ready
        def set_focus():
            try:
                self.focus_set()
                self.canvas.focus_set()
            except:
                pass
        self.after(200, set_focus)

    # center_window removed as it is handled by the main app window

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg='#1e1e1e', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#1e1e1e')
        header_content.pack(fill=tk.BOTH, expand=True, padx=50, pady=15)
        
        tk.Label(header_content, text="Your Library", font=("Arial", 24, "bold"), 
                 bg='#1e1e1e', fg='white').pack(side=tk.LEFT)

        # Horizontal scrollable canvas for cards (no scrollbar visible)
        canvas_frame = tk.Frame(self, bg='#1e1e1e')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(0, 20))
        
        self.canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', highlightthickness=0, bd=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#1e1e1e')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure for horizontal scrolling only
        self.canvas.configure(xscrollcommand=lambda *args: None)  # No scrollbar
        
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Track scroll position for smooth animation
        self.target_x = 0
        self.current_x = 0
        self.scroll_speed = 0.15  # Animation speed (0-1)
        
        # Bind mousewheel for horizontal scrolling
        def on_mousewheel(event):
            try:
                if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                    # Windows and Mac - scroll horizontally
                    if event.delta:
                        delta = int(-1 * (event.delta / 120))
                        self.smooth_scroll_horizontal(delta * 50)  # Scroll 50 pixels per wheel tick
                    # Linux
                    elif event.num == 4:
                        self.smooth_scroll_horizontal(-50)
                    elif event.num == 5:
                        self.smooth_scroll_horizontal(50)
            except (tk.TclError, AttributeError):
                pass
        
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        # Also bind to canvas frame for Linux
        canvas_frame.bind("<Button-4>", lambda e: self.smooth_scroll_horizontal(-50) if hasattr(self, 'canvas') else None)
        canvas_frame.bind("<Button-5>", lambda e: self.smooth_scroll_horizontal(50) if hasattr(self, 'canvas') else None)
        
        # Footer with keyboard hints
        footer = tk.Frame(self, bg='#1e1e1e', height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        hint_text = "← → Navigate  •  Enter Open/Create"
        tk.Label(footer, text=hint_text, bg='#1e1e1e', fg='#666666',
                font=("Arial", 9)).pack(pady=10)
        
        # Keyboard bindings - horizontal navigation (left/right)
        def on_left(event=None):
            result = self.navigate(-1)
            return result if result else "break"
        
        def on_right(event=None):
            result = self.navigate(1)
            return result if result else "break"
        
        def on_enter(event=None):
            self.open_selected()
            return "break"
        
        # Bind to self (frame)
        self.bind('<Left>', on_left)
        self.bind('<Right>', on_right)
        self.bind('<Return>', on_enter)
        self.bind('<Escape>', lambda e: self.master.quit())
        
        # Also bind to master window for when focus is elsewhere
        self.master.bind('<Left>', on_left)
        self.master.bind('<Right>', on_right)
        self.master.bind('<Return>', on_enter)
        
        # Bind to canvas and scrollable frame too
        self.canvas.bind('<Left>', on_left)
        self.canvas.bind('<Right>', on_right)
        self.canvas.bind('<Return>', on_enter)
        self.scrollable_frame.bind('<Left>', on_left)
        self.scrollable_frame.bind('<Right>', on_right)
        self.scrollable_frame.bind('<Return>', on_enter)
    

    def load_projects(self):
        # Clear existing cards
        for card in self.book_cards:
            card.destroy()
        self.book_cards = []
        self.book_paths = []
        self.selected_index = -1
        
        book_dirs = self.file_manager.list_books()
        print(f"Found book directories: {book_dirs}") # Debug
        
        # Always show the new book card, even if no books exist
        # (The new book card will be added below)
        
        # Create cards in a horizontal row layout (no grid, just pack horizontally)
        cards_container = tk.Frame(self.scrollable_frame, bg='#1e1e1e')
        cards_container.pack(fill=tk.Y, side=tk.LEFT, padx=20, pady=20)
        
        # Add book cards first
        for i, book_dir in enumerate(book_dirs):
            book_path = os.path.join(self.file_manager.base_path, book_dir)
            book_stats = self.file_manager.get_book_statistics(book_path)
            
            if book_stats:
                self.book_paths.append(book_path)
                
                # Create card - use a closure to capture the index correctly
                def make_click_handler(index):
                    return lambda: self.select_book(index)
                
                card = BookCard(cards_container, book_stats, 
                               make_click_handler(i),
                               is_selected=(i == 0))
                
                # Pack horizontally
                card.pack(side=tk.LEFT, padx=15, pady=15, fill=tk.Y)
                
                self.book_cards.append(card)
        
        # Add "New Book" card at the end
        new_book_card = NewBookCard(cards_container, self.start_new_book, is_selected=False)
        new_book_card.pack(side=tk.LEFT, padx=15, pady=15, fill=tk.Y)
        self.book_cards.append(new_book_card)
        self.book_paths.append(None)  # None indicates this is the new book card
        
        # Select first book card by default (not the new book card)
        if len(self.book_cards) > 1:  # More than just the new book card
            self.selected_index = 0
            self.book_cards[0].set_selected(True)
        elif len(self.book_cards) == 1:  # Only new book card
            self.selected_index = 0
            self.book_cards[0].set_selected(True)
        
        # Ensure focus is set for keyboard navigation
        self.after(100, self.ensure_focus)
        
        # Start smooth scroll animation loop
        self.animate_scroll()
    
    def ensure_focus(self):
        """Ensure this frame has focus for keyboard navigation"""
        self.focus_set()
        self.canvas.focus_set()
    
    def navigate(self, direction):
        """Navigate between books with arrow keys"""
        if not self.book_cards:
            return
        
        # Deselect current
        if 0 <= self.selected_index < len(self.book_cards):
            self.book_cards[self.selected_index].set_selected(False)
        
        # Move selection
        self.selected_index += direction
        self.selected_index = max(0, min(self.selected_index, len(self.book_cards) - 1))
        
        # Select new
        self.book_cards[self.selected_index].set_selected(True)
        
        # Scroll into view
        self.scroll_to_selected()
        
        # Return "break" to prevent event propagation
        return "break"
    
    def smooth_scroll_horizontal(self, delta):
        """Smoothly scroll horizontally by delta pixels"""
        self.target_x += delta
        self.target_x = max(0, self.target_x)  # Don't scroll past start
    
    def animate_scroll(self):
        """Animate smooth horizontal scrolling"""
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            try:
                # Smooth interpolation using easing
                diff = self.target_x - self.current_x
                if abs(diff) > 1:
                    # Ease out animation
                    self.current_x += diff * self.scroll_speed
                    frame_width = max(1, self.scrollable_frame.winfo_reqwidth())
                    if frame_width > 0:
                        self.canvas.xview_moveto(self.current_x / frame_width)
                else:
                    self.current_x = self.target_x
                    frame_width = max(1, self.scrollable_frame.winfo_reqwidth())
                    if frame_width > 0:
                        self.canvas.xview_moveto(self.current_x / frame_width)
            except (tk.TclError, AttributeError):
                pass
        
        # Continue animation
        self.after(16, self.animate_scroll)  # ~60fps
    
    def scroll_to_selected(self):
        """Scroll canvas horizontally to show selected card with smooth animation"""
        if 0 <= self.selected_index < len(self.book_cards):
            try:
                self.canvas.update_idletasks()
                card = self.book_cards[self.selected_index]
                card.update_idletasks()
                
                # Get card position relative to scrollable frame
                card_x = card.winfo_x()
                card_width = card.winfo_width()
                canvas_width = self.canvas.winfo_width()
                frame_width = max(1, self.scrollable_frame.winfo_reqwidth())
                
                # Calculate target scroll position to center the card in viewport
                target_x = card_x + (card_width / 2) - (canvas_width / 2)
                target_x = max(0, min(target_x, max(0, frame_width - canvas_width)))
                
                # Set target for smooth scrolling animation
                self.target_x = target_x
            except (tk.TclError, AttributeError):
                pass
    
    def select_book(self, index):
        """Select a book by index"""
        if 0 <= index < len(self.book_cards):
            # Deselect current
            if 0 <= self.selected_index < len(self.book_cards):
                self.book_cards[self.selected_index].set_selected(False)
            
            # Select new
            self.selected_index = index
            self.book_cards[index].set_selected(True)
            self.open_selected()

    def start_new_book(self):
        self.master.show_book_wizard()

    def open_selected(self, event=None):
        """Open the currently selected book or create new book"""
        if 0 <= self.selected_index < len(self.book_paths):
            project_path = self.book_paths[self.selected_index]
            if project_path is None:
                # This is the "New Book" card
                self.start_new_book()
            else:
                self.on_project_selected(project_path)
