import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path

class BookWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Writer")
        
        # Configure for 1080x400 screen
        self.root.geometry("1080x400")
        
        # Variables
        self.current_file = None
        self.modified = False
        
        # Key bindings configuration
        self.key_bindings = {
            # Layer 1: Basic editing (no modifier)
            '<Escape>': self.toggle_sidebar,
            '<Return>': self.smart_return,
            
            # Layer 2: File operations (Fn + key)
            '<Control-s>': self.save_file,
            '<Control-n>': self.new_file,
            '<Control-o>': self.open_file,
            
            # Layer 3: Formatting (Fn + Shift + key)
            '<Control-b>': lambda: self.format_text('bold'),
            '<Control-i>': lambda: self.format_text('italic'),
            
            # Layer 4: Navigation (Fn + Alt + key)
            '<Alt-h>': self.goto_previous_section,
            '<Alt-l>': self.goto_next_section,
        }
        
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        # Main layout with flexibile grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sidebar (initially hidden)
        self.sidebar = ttk.Frame(self.root, width=200)
        self.setup_sidebar()
        
        # Main editor
        self.editor = tk.Text(self.root, wrap=tk.WORD, undo=True)
        self.editor.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready | Press Esc for menu")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
    def setup_sidebar(self):
        # Chapter list
        self.chapter_list = ttk.Treeview(self.sidebar, show="tree")
        self.chapter_list.pack(expand=True, fill="both")
        
        # Quick command palette (triggered by Ctrl+P)
        self.command_entry = ttk.Entry(self.sidebar)
        self.command_entry.pack(fill="x", padx=5, pady=5)
    
    def setup_bindings(self):
        for key, command in self.key_bindings.items():
            self.root.bind(key, command)
            self.editor.bind(key, command)
    
    def toggle_sidebar(self, event=None):
        if self.sidebar.winfo_viewable():
            self.sidebar.grid_remove()
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
        return "break"
    
    def smart_return(self, event=None):
        # Handle auto-continuation of lists and other markdown elements
        current_line = self.editor.get("insert linestart", "insert lineend")
        if current_line.startswith("- "):
            self.editor.insert("insert", "\n- ")
            return "break"
        return None
    
    def save_file(self, event=None):
        if not self.current_file:
            self.current_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not self.current_file:
                return "break"
        
        content = self.editor.get("1.0", tk.END)
        try:
            with open(self.current_file, 'w') as f:
                f.write(content)
            self.modified = False
            self.update_status(f"Saved: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
        return "break"
    
    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.editor.delete('1.0', tk.END)
                self.editor.insert('1.0', content)
                self.current_file = file_path
                self.update_status(f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        return "break"
    
    def new_file(self, event=None):
        if self.modified:
            if messagebox.askyesno("Save Changes?", 
                "Current file has unsaved changes. Save before creating new file?"):
                self.save_file()
        
        self.editor.delete('1.0', tk.END)
        self.current_file = None
        self.modified = False
        self.update_status("New File")
        return "break"
    
    def format_text(self, style):
        if style == 'bold':
            self.editor.insert(tk.INSERT, "**")
            # Move cursor back one character
            self.editor.mark_set(tk.INSERT, f"{tk.INSERT}-1c")
        elif style == 'italic':
            self.editor.insert(tk.INSERT, "_")
        return "break"
    
    def goto_previous_section(self, event=None):
        # Implement section navigation
        return "break"
    
    def goto_next_section(self, event=None):
        # Implement section navigation
        return "break"
    
    def update_status(self, message):
        self.status_bar.config(text=message)

def main():
    root = tk.Tk()
    app = BookWriter(root)
    root.mainloop()

if __name__ == "__main__":
    main()