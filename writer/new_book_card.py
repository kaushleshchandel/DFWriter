import tkinter as tk

class NewBookCard(tk.Frame):
    """Large plus sign card for creating new books"""
    def __init__(self, parent, on_click, is_selected=False):
        super().__init__(parent, bg='#1e1e1e', relief=tk.FLAT, bd=0)
        
        self.on_click = on_click
        self.is_selected = is_selected
        
        # Card styling
        if is_selected:
            self.card_bg = '#3a4a5a'
            self.border_color = '#5a9fd4'
            self.plus_color = '#b0d4f0'
        else:
            self.card_bg = '#252525'
            self.border_color = '#252525'
            self.plus_color = '#666666'
        
        self.hover_bg = '#2d3d4d'
        self.current_bg = self.card_bg
        
        self.configure(bg=self.card_bg, relief=tk.FLAT, bd=0, cursor='hand2', width=350)
        
        self.create_card()
        self.bind_events()
    
    def create_card(self):
        # Main card container with border for selected state
        border_width = 3 if self.is_selected else 0
        card_container = tk.Frame(self, bg=self.border_color if self.is_selected else '#1e1e1e',
                                  relief=tk.FLAT, bd=border_width)
        card_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Inner content frame
        inner_frame = tk.Frame(card_container, bg=self.current_bg, relief=tk.FLAT)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=border_width, pady=border_width)
        
        # Center the plus sign
        center_frame = tk.Frame(inner_frame, bg=self.current_bg)
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # Large plus sign using a canvas
        plus_size = 80
        plus_canvas = tk.Canvas(center_frame, bg=self.current_bg, highlightthickness=0,
                               width=plus_size, height=plus_size)
        plus_canvas.pack(expand=True)
        
        # Draw plus sign
        line_width = 8
        center = plus_size // 2
        
        # Horizontal line
        plus_canvas.create_line(center - plus_size//3, center,
                               center + plus_size//3, center,
                               fill=self.plus_color, width=line_width, capstyle=tk.ROUND)
        
        # Vertical line
        plus_canvas.create_line(center, center - plus_size//3,
                               center, center + plus_size//3,
                               fill=self.plus_color, width=line_width, capstyle=tk.ROUND)
        
        # "New Book" text below
        text_label = tk.Label(center_frame, text="New Book",
                             bg=self.current_bg, fg=self.plus_color,
                             font=("Arial", 12, "bold"))
        text_label.pack(pady=(10, 0))
        
        # Store references
        self.card_container = card_container
        self.inner_frame = inner_frame
        self.plus_canvas = plus_canvas
        self.text_label = text_label
    
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
            self.card_bg = '#3a4a5a'
            self.border_color = '#5a9fd4'
            self.plus_color = '#b0d4f0'
        else:
            self.card_bg = '#252525'
            self.border_color = '#252525'
            self.plus_color = '#666666'
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
        
        # Update inner frame
        widgets = [self.inner_frame, self.text_label]
        for widget in widgets:
            if hasattr(widget, 'config'):
                try:
                    widget.config(bg=self.current_bg)
                except:
                    pass
        
        # Update text color
        if hasattr(self, 'text_label'):
            try:
                self.text_label.config(fg=self.plus_color)
            except:
                pass
        
        # Redraw plus sign
        if hasattr(self, 'plus_canvas'):
            try:
                self.plus_canvas.delete("all")
                plus_size = 80
                line_width = 8
                center = plus_size // 2
                
                # Horizontal line
                self.plus_canvas.create_line(center - plus_size//3, center,
                                           center + plus_size//3, center,
                                           fill=self.plus_color, width=line_width, capstyle=tk.ROUND)
                
                # Vertical line
                self.plus_canvas.create_line(center, center - plus_size//3,
                                           center, center + plus_size//3,
                                           fill=self.plus_color, width=line_width, capstyle=tk.ROUND)
            except:
                pass


