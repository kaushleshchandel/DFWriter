import tkinter as tk
from wide_dialogs import WideScreenMessageDialog

class ChapterNameDialog(tk.Toplevel):
    """Dialog to get chapter name from user"""
    def __init__(self, parent, title="New Chapter"):
        super().__init__(parent)
        self.result = None
        
        self.configure(bg='#1e1e1e')
        self.title(title)
        
        # Get parent window dimensions
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 1280
        parent_height = parent.winfo_height() if parent.winfo_height() > 1 else 400
        
        dialog_width = 500
        dialog_height = 200
        
        x = parent.winfo_x() + (parent_width - dialog_width) // 2
        y = parent.winfo_y() + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.transient(parent)
        self.grab_set()
        self.attributes('-topmost', True)
        
        self.create_widgets()
        
        # Keyboard bindings
        self.bind('<Return>', lambda e: self.confirm())
        self.bind('<Escape>', lambda e: self.cancel())
        self.bind('<Tab>', self.on_tab)
        
        # Focus on entry and dialog
        self.after(50, self.setup_focus)
    
    def setup_focus(self):
        """Set focus on dialog and entry field"""
        self.focus_set()
        self.chapter_entry.focus_set()
    
    def on_tab(self, event=None):
        """Tab to cycle between entry and buttons"""
        # Get current focus
        focused = self.focus_get()
        
        if focused == self.chapter_entry:
            # Move focus to Create button
            self.confirm_btn.focus_set()
        elif focused == self.confirm_btn:
            # Move focus to Cancel button
            self.cancel_btn.focus_set()
        else:
            # Move focus back to entry
            self.chapter_entry.focus_set()
        return "break"
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg='#282c34', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="New Chapter", font=("Arial", 12, "bold"),
                bg='#282c34', fg='white').pack(pady=10)
        
        # Content
        content = tk.Frame(self, bg='#1e1e1e')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(content, text="Enter Chapter Name:", bg='#1e1e1e', fg='white',
                font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 10))
        
        self.chapter_name = tk.StringVar()
        self.chapter_entry = tk.Entry(content, textvariable=self.chapter_name,
                                     bg='#282c34', fg='white', insertbackground='white',
                                     font=("Arial", 11), borderwidth=1, relief=tk.SOLID)
        self.chapter_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(self, bg='#1e1e1e', height=50)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)
        
        self.cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel,
                             bg='#3e4451', fg='white', font=("Arial", 10),
                             padx=20, pady=5, bd=0, activebackground='#4a5567',
                             highlightthickness=2, highlightbackground='#3e4451',
                             highlightcolor='#61afef')
        self.cancel_btn.pack(side=tk.RIGHT, padx=10, pady=15)
        
        self.confirm_btn = tk.Button(button_frame, text="Create", command=self.confirm,
                              bg='#3e4451', fg='white', font=("Arial", 10),
                              padx=20, pady=5, bd=0, activebackground='#4a5567',
                              highlightthickness=2, highlightbackground='#3e4451',
                              highlightcolor='#61afef')
        self.confirm_btn.pack(side=tk.RIGHT, padx=10, pady=15)
    
    def confirm(self):
        """Confirm chapter name"""
        name = self.chapter_name.get().strip()
        if not name:
            WideScreenMessageDialog.showerror(self.master, "Error", "Chapter name cannot be empty")
            return
        
        # Sanitize chapter name for filesystem
        safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()
        safe_name = safe_name.replace(' ', '_')  # Replace spaces with underscores
        
        if not safe_name:
            WideScreenMessageDialog.showerror(self.master, "Error", "Invalid chapter name")
            return
        
        self.result = safe_name
        self.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.destroy()
    
    @staticmethod
    def ask_chapter_name(parent):
        """Static method to get chapter name"""
        dialog = ChapterNameDialog(parent)
        parent.wait_window(dialog)
        return dialog.result

