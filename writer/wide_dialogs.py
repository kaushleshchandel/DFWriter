import tkinter as tk
from tkinter import ttk
import os

class WideScreenFileDialog(tk.Toplevel):
    """Custom wide-screen file dialog matching the app's design"""
    def __init__(self, parent, mode='open', title="Select File", initialdir=None, filetypes=None):
        super().__init__(parent)
        self.result = None
        self.mode = mode  # 'open' or 'save'
        
        # Configure dialog to match app's wide-screen design
        self.configure(bg='#1e1e1e')
        self.title(title)
        
        # Get parent window dimensions for wide-screen layout
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 1280
        parent_height = parent.winfo_height() if parent.winfo_height() > 1 else 400
        
        # Use wide-screen dimensions
        dialog_width = min(1200, parent_width - 80)
        dialog_height = min(500, parent_height - 80)
        
        # Center on parent
        x = parent.winfo_x() + (parent_width - dialog_width) // 2
        y = parent.winfo_y() + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.transient(parent)
        self.grab_set()
        
        # Make it modal and match app style
        self.attributes('-topmost', True)
        
        # Set initial directory
        self.current_dir = initialdir or os.path.expanduser("~")
        if not os.path.exists(self.current_dir):
            self.current_dir = os.path.expanduser("~")
        
        self.filetypes = filetypes or [("All Files", "*.*")]
        self.selected_file = tk.StringVar()
        
        self.create_widgets()
        self.load_directory()
        
        # Keyboard bindings
        self.bind('<Return>', lambda e: self.confirm())
        self.bind('<Escape>', lambda e: self.cancel())
        self.bind('<Up>', lambda e: self.navigate_listbox(-1))
        self.bind('<Down>', lambda e: self.navigate_listbox(1))
        self.file_listbox.bind('<Return>', lambda e: self.on_double_click())
        
        # Focus on dialog and entry
        self.after(50, self.setup_focus)
    
    def setup_focus(self):
        """Set focus on dialog and entry field"""
        self.focus_set()
        self.filename_entry.focus_set()
    
    def navigate_listbox(self, direction):
        """Navigate listbox with arrow keys"""
        current = self.file_listbox.curselection()
        if current:
            index = current[0] + direction
        else:
            index = 0 if direction > 0 else self.file_listbox.size() - 1
        
        if 0 <= index < self.file_listbox.size():
            self.file_listbox.selection_clear(0, 'end')
            self.file_listbox.selection_set(index)
            self.file_listbox.see(index)
            # Update filename entry
            item = self.file_listbox.get(index)
            if item != ".. (Parent Directory)":
                if item.startswith("📁 "):
                    item = item[2:]
                self.selected_file.set(item)
        return "break"
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg='#282c34', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=self.title(), font=("Arial", 12, "bold"),
                bg='#282c34', fg='white').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Main content area
        content = tk.Frame(self, bg='#1e1e1e')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current directory display
        dir_frame = tk.Frame(content, bg='#282c34', height=30)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        dir_frame.pack_propagate(False)
        
        self.dir_label = tk.Label(dir_frame, text=self.current_dir, 
                                  bg='#282c34', fg='white', font=("Arial", 9),
                                  anchor='w', padx=10)
        self.dir_label.pack(fill=tk.X, padx=5, pady=5)
        
        # File list with scrollbar
        list_frame = tk.Frame(content, bg='#1e1e1e')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, 
                                      bg='#282c34', fg='white',
                                      selectbackground='#4e5563',
                                      font=("Arial", 10),
                                      yscrollcommand=scrollbar.set,
                                      borderwidth=0, highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.bind('<Double-Button-1>', self.on_double_click)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_select)
        self.file_listbox.bind('<Button-1>', self.on_select)
        
        # Filename entry
        entry_frame = tk.Frame(content, bg='#1e1e1e')
        entry_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(entry_frame, text="Filename:", bg='#1e1e1e', fg='white',
                font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.filename_entry = tk.Entry(entry_frame, textvariable=self.selected_file,
                                      bg='#282c34', fg='white', insertbackground='white',
                                      font=("Arial", 10), borderwidth=1, relief=tk.SOLID)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.filename_entry.bind('<KeyRelease>', self.on_entry_change)
        self.filename_entry.bind('<Return>', lambda e: self.confirm())
        
        # File type filter
        if len(self.filetypes) > 1:
            filter_frame = tk.Frame(content, bg='#1e1e1e')
            filter_frame.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(filter_frame, text="File Type:", bg='#1e1e1e', fg='white',
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
            
            self.filter_var = tk.StringVar(value=self.filetypes[0][0])
            filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                       values=[ft[0] for ft in self.filetypes],
                                       state='readonly', width=20)
            filter_combo.pack(side=tk.LEFT)
            filter_combo.bind('<<ComboboxSelected>>', lambda e: self.load_directory())
        
        # Buttons
        button_frame = tk.Frame(self, bg='#1e1e1e', height=50)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel,
                             bg='#3e4451', fg='white', font=("Arial", 10),
                             padx=20, pady=5, bd=0, activebackground='#4a5567')
        cancel_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        confirm_text = "Save" if self.mode == 'save' else "Open"
        self.confirm_btn = tk.Button(button_frame, text=confirm_text, command=self.confirm,
                                    bg='#3e4451', fg='white', font=("Arial", 10),
                                    padx=20, pady=5, bd=0, activebackground='#4a5567')
        self.confirm_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def load_directory(self):
        """Load files and directories from current directory"""
        self.file_listbox.delete(0, tk.END)
        
        try:
            # Add parent directory option
            if self.current_dir != os.path.dirname(self.current_dir):
                self.file_listbox.insert(tk.END, ".. (Parent Directory)")
            
            # Get current filter
            current_filter = None
            if hasattr(self, 'filter_var'):
                filter_name = self.filter_var.get()
                for ft in self.filetypes:
                    if ft[0] == filter_name:
                        current_filter = ft[1]
                        break
            
            items = []
            for item in sorted(os.listdir(self.current_dir)):
                item_path = os.path.join(self.current_dir, item)
                if os.path.isdir(item_path):
                    items.append(("📁 " + item, item_path, True))
                elif current_filter is None or self.matches_filter(item, current_filter):
                    items.append((item, item_path, False))
            
            for display, path, is_dir in items:
                self.file_listbox.insert(tk.END, display)
            
            self.dir_label.config(text=self.current_dir)
        except PermissionError:
            self.file_listbox.insert(tk.END, "Permission Denied")
    
    def matches_filter(self, filename, pattern):
        """Check if filename matches the filter pattern"""
        if pattern == "*.*":
            return True
        extensions = pattern.split(";")
        for ext in extensions:
            ext = ext.strip().lstrip("*")
            if filename.lower().endswith(ext.lower()):
                return True
        return False
    
    def on_select(self, event=None):
        """Handle file selection"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.file_listbox.get(index)
            
            # Handle parent directory
            if item == ".. (Parent Directory)":
                return
            
            # Remove folder icon prefix if present
            if item.startswith("📁 "):
                item = item[2:]
            
            item_path = os.path.join(self.current_dir, item)
            if os.path.isdir(item_path):
                return
            
            self.selected_file.set(item)
    
    def on_double_click(self, event=None):
        """Handle double-click on listbox item"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.file_listbox.get(index)
            
            # Handle parent directory
            if item == ".. (Parent Directory)":
                parent = os.path.dirname(self.current_dir)
                if os.path.exists(parent):
                    self.current_dir = parent
                    self.load_directory()
                return
            
            # Remove folder icon prefix if present
            if item.startswith("📁 "):
                item = item[2:]
            
            item_path = os.path.join(self.current_dir, item)
            
            if os.path.isdir(item_path):
                self.current_dir = item_path
                self.load_directory()
            else:
                self.selected_file.set(item)
                if self.mode == 'open':
                    self.confirm()
    
    def on_entry_change(self, event=None):
        """Handle entry field changes"""
        # Update confirm button state based on entry
        filename = self.selected_file.get().strip()
        if filename:
            self.confirm_btn.config(state=tk.NORMAL)
        else:
            self.confirm_btn.config(state=tk.NORMAL)  # Allow empty for directory navigation
    
    def confirm(self):
        """Confirm file selection"""
        filename = self.selected_file.get().strip()
        if not filename:
            return
        
        # If no path separator, use current directory
        if os.path.sep not in filename:
            file_path = os.path.join(self.current_dir, filename)
        else:
            file_path = filename
        
        # For save mode, check if directory exists
        if self.mode == 'save':
            dir_path = os.path.dirname(file_path) if os.path.dirname(file_path) else self.current_dir
            if not os.path.exists(dir_path):
                return
        
        self.result = file_path
        self.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.destroy()
    
    @staticmethod
    def askopenfilename(parent, title="Open File", initialdir=None, filetypes=None):
        """Static method to match tkinter filedialog interface"""
        dialog = WideScreenFileDialog(parent, mode='open', title=title, 
                                      initialdir=initialdir, filetypes=filetypes)
        parent.wait_window(dialog)
        return dialog.result
    
    @staticmethod
    def asksaveasfilename(parent, title="Save File", initialdir=None, 
                         defaultextension="", filetypes=None):
        """Static method to match tkinter filedialog interface"""
        dialog = WideScreenFileDialog(parent, mode='save', title=title,
                                     initialdir=initialdir, filetypes=filetypes)
        if defaultextension and not dialog.selected_file.get().endswith(defaultextension):
            dialog.selected_file.set(dialog.selected_file.get() + defaultextension)
        parent.wait_window(dialog)
        return dialog.result


class WideScreenMessageDialog(tk.Toplevel):
    """Custom wide-screen message dialog with full keyboard support"""
    def __init__(self, parent, title="Message", message="", buttons=["OK"]):
        super().__init__(parent)
        self.result = None
        self.buttons = buttons
        self.button_widgets = []
        self.focused_button_index = 0  # Focus on first button (leftmost)
        
        self.configure(bg='#1e1e1e')
        self.title(title)
        
        # Wide-screen dimensions
        parent_width = parent.winfo_width() if parent.winfo_width() > 1 else 1280
        parent_height = parent.winfo_height() if parent.winfo_height() > 1 else 400
        
        dialog_width = min(600, parent_width - 100)
        dialog_height = 200
        
        x = parent.winfo_x() + (parent_width - dialog_width) // 2
        y = parent.winfo_y() + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.transient(parent)
        self.grab_set()
        self.attributes('-topmost', True)
        
        # Header
        header = tk.Frame(self, bg='#282c34', height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=title, font=("Arial", 12, "bold"),
                bg='#282c34', fg='white').pack(pady=10)
        
        # Message
        content = tk.Frame(self, bg='#1e1e1e')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(content, text=message, bg='#1e1e1e', fg='white',
                font=("Arial", 10), wraplength=dialog_width-60, justify=tk.LEFT).pack()
        
        # Buttons (reversed so leftmost is first in list)
        button_frame = tk.Frame(self, bg='#1e1e1e', height=50)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)
        
        # Store buttons in reverse order (right to left) but track them normally
        for i, btn_text in enumerate(reversed(buttons)):
            btn = tk.Button(button_frame, text=btn_text, 
                           command=lambda t=btn_text: self.button_click(t),
                           bg='#3e4451', fg='white', font=("Arial", 10),
                           padx=20, pady=5, bd=0, activebackground='#4a5567',
                           highlightthickness=2, highlightbackground='#3e4451',
                           highlightcolor='#61afef')
            btn.pack(side=tk.RIGHT, padx=5, pady=10)
            self.button_widgets.append(btn)
        
        # Reverse button_widgets to match button order (leftmost is index 0)
        self.button_widgets = list(reversed(self.button_widgets))
        
        # Keyboard bindings
        self.bind('<Return>', self.on_enter)
        self.bind('<Escape>', self.on_escape)
        self.bind('<Left>', self.on_left)
        self.bind('<Right>', self.on_right)
        self.bind('<Tab>', self.on_tab)
        
        # Focus the dialog and first button
        self.after(50, self.setup_focus)
    
    def setup_focus(self):
        """Set focus on dialog and highlight first button"""
        self.focus_set()
        self.update_focus_highlight()
    
    def update_focus_highlight(self):
        """Update button highlighting based on focused button"""
        for i, btn in enumerate(self.button_widgets):
            if i == self.focused_button_index:
                btn.config(bg='#4a5567', highlightbackground='#61afef')
            else:
                btn.config(bg='#3e4451', highlightbackground='#3e4451')
    
    def on_enter(self, event=None):
        """Press Enter to confirm focused button"""
        if 0 <= self.focused_button_index < len(self.buttons):
            self.button_click(self.buttons[self.focused_button_index])
        return "break"
    
    def on_escape(self, event=None):
        """Press Escape to select last button (usually Cancel/No)"""
        if len(self.buttons) > 1:
            self.button_click(self.buttons[-1])
        else:
            self.button_click(self.buttons[0])
        return "break"
    
    def on_left(self, event=None):
        """Navigate left between buttons"""
        if len(self.button_widgets) > 1:
            self.focused_button_index = (self.focused_button_index - 1) % len(self.button_widgets)
            self.update_focus_highlight()
        return "break"
    
    def on_right(self, event=None):
        """Navigate right between buttons"""
        if len(self.button_widgets) > 1:
            self.focused_button_index = (self.focused_button_index + 1) % len(self.button_widgets)
            self.update_focus_highlight()
        return "break"
    
    def on_tab(self, event=None):
        """Tab to cycle through buttons"""
        if len(self.button_widgets) > 1:
            self.focused_button_index = (self.focused_button_index + 1) % len(self.button_widgets)
            self.update_focus_highlight()
        return "break"
    
    def button_click(self, button_text):
        self.result = button_text
        self.destroy()
    
    @staticmethod
    def showinfo(parent, title="Information", message=""):
        dialog = WideScreenMessageDialog(parent, title, message, ["OK"])
        parent.wait_window(dialog)
    
    @staticmethod
    def showwarning(parent, title="Warning", message=""):
        dialog = WideScreenMessageDialog(parent, title, message, ["OK"])
        parent.wait_window(dialog)
    
    @staticmethod
    def showerror(parent, title="Error", message=""):
        dialog = WideScreenMessageDialog(parent, title, message, ["OK"])
        parent.wait_window(dialog)
    
    @staticmethod
    def askyesno(parent, title="Question", message=""):
        dialog = WideScreenMessageDialog(parent, title, message, ["Yes", "No"])
        parent.wait_window(dialog)
        return dialog.result == "Yes"

