import tkinter as tk
from datetime import datetime

class BookCard(tk.Frame):
    """Material Design style book card with progress indicator"""
    def __init__(self, parent, book_stats, on_click, is_selected=False):
        super().__init__(parent, bg='#1e1e1e', relief=tk.FLAT, bd=0)
        
        self.book_stats = book_stats
        self.on_click = on_click
        self.is_selected = is_selected
        
        # Card styling - more colorful when selected
        if is_selected:
            self.card_bg = '#3a4a5a'  # Blue-gray for selected
            self.border_color = '#5a9fd4'  # Bright blue border
            self.title_color = '#ffffff'
            self.genre_color = '#b0d4f0'
        else:
            self.card_bg = '#252525'
            self.border_color = '#252525'
            self.title_color = '#ffffff'
            self.genre_color = '#888888'
        
        self.hover_bg = '#2d3d4d'
        self.current_bg = self.card_bg
        
        self.configure(bg=self.card_bg, relief=tk.FLAT, bd=0, cursor='hand2')
        
        # Set minimum width for cards
        self.configure(width=350)
        
        self.create_card()
        self.bind_events()
    
    def create_card(self):
        # Main card container with padding and border for selected state
        border_width = 3 if self.is_selected else 0
        card_container = tk.Frame(self, bg=self.border_color if self.is_selected else '#1e1e1e', 
                                  relief=tk.FLAT, bd=border_width)
        card_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Inner content frame
        inner_frame = tk.Frame(card_container, bg=self.current_bg, relief=tk.FLAT)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=border_width, pady=border_width)
        
        # Title and genre
        header_frame = tk.Frame(inner_frame, bg=self.current_bg)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(header_frame, text=self.book_stats['title'],
                              bg=self.current_bg, fg=self.title_color,
                              font=("Arial", 14, "bold"), anchor='w')
        title_label.pack(fill=tk.X)
        
        genre_label = tk.Label(header_frame, text=self.book_stats['genre'],
                              bg=self.current_bg, fg=self.genre_color,
                              font=("Arial", 10), anchor='w')
        genre_label.pack(fill=tk.X, pady=(2, 0))
        
        # Progress bar
        progress_frame = tk.Frame(inner_frame, bg=self.current_bg)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Progress text
        progress_text = f"{self.book_stats['total_words']:,} / {self.book_stats['target_words']:,} words"
        progress_label = tk.Label(progress_frame, text=progress_text,
                                  bg=self.current_bg, fg='#aaaaaa',
                                  font=("Arial", 9), anchor='w')
        progress_label.pack(fill=tk.X, pady=(0, 5))
        
        # Progress bar background
        bar_bg = tk.Frame(progress_frame, bg='#1a1a1a', height=8, relief=tk.FLAT)
        bar_bg.pack(fill=tk.X)
        bar_bg.pack_propagate(False)
        
        # Progress bar fill - use a canvas for better control
        progress_pct = min(1.0, max(0.0, self.book_stats['progress'] / 100.0))
        if progress_pct > 0:
            # Use a simple frame that will be sized by pack
            bar_fill = tk.Frame(bar_bg, bg='#4CAF50', height=8)
            bar_fill.place(relx=0, rely=0, relwidth=progress_pct, relheight=1.0)
        
        # Statistics row
        stats_frame = tk.Frame(inner_frame, bg=self.current_bg)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        stats = [
            f"{self.book_stats['total_chapters']} chapters",
            f"{self.book_stats['total_pages']} pages",
            f"{self.book_stats['progress']}%"
        ]
        
        for i, stat in enumerate(stats):
            stat_label = tk.Label(stats_frame, text=stat,
                                 bg=self.current_bg, fg='#666666',
                                 font=("Arial", 9))
            stat_label.pack(side=tk.LEFT)
            if i < len(stats) - 1:
                tk.Label(stats_frame, text=" • ", bg=self.current_bg, fg='#666666',
                        font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Store references for hover effects
        self.card_container = card_container
        self.inner_frame = inner_frame
        self.title_label = title_label
        self.genre_label = genre_label
        self.progress_label = progress_label
        self.stats_frame = stats_frame
        self.bar_bg = bar_bg
    
    def bind_events(self):
        """Bind mouse and keyboard events"""
        for widget in [self, self.card_container, self.inner_frame]:
            widget.bind('<Button-1>', lambda e: self.on_click())
            widget.bind('<Enter>', lambda e: self.on_hover(True))
            widget.bind('<Leave>', lambda e: self.on_hover(False))
    
    def on_hover(self, enter):
        """Handle hover effects"""
        if not self.is_selected:
            self.current_bg = self.hover_bg if enter else self.card_bg
            self.update_colors()
    
    def set_selected(self, selected):
        """Update selection state"""
        self.is_selected = selected
        if selected:
            self.card_bg = '#3a4a5a'  # Blue-gray for selected
            self.border_color = '#5a9fd4'  # Bright blue border
            self.title_color = '#ffffff'
            self.genre_color = '#b0d4f0'
        else:
            self.card_bg = '#252525'
            self.border_color = '#252525'
            self.title_color = '#ffffff'
            self.genre_color = '#888888'
        self.current_bg = self.card_bg
        self.update_colors()
    
    def update_colors(self):
        """Update all widget colors"""
        # Update border
        if hasattr(self, 'card_container'):
            try:
                border_width = 3 if self.is_selected else 0
                self.card_container.config(bg=self.border_color, bd=border_width)
            except:
                pass
        
        # Update inner frame and content
        widgets = [
            self.inner_frame, self.title_label, self.genre_label,
            self.progress_label, self.stats_frame, self.bar_bg
        ]
        for widget in widgets:
            if hasattr(widget, 'config'):
                try:
                    widget.config(bg=self.current_bg)
                except:
                    pass
        
        # Update text colors
        if hasattr(self, 'title_label'):
            try:
                self.title_label.config(fg=self.title_color)
            except:
                pass
        if hasattr(self, 'genre_label'):
            try:
                self.genre_label.config(fg=self.genre_color)
            except:
                pass

