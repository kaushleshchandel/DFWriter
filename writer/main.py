import tkinter as tk
import platform
from dfwriter import DFWriter
from project_picker import ProjectPicker
from book_wizard import BookWizard
from file_operations import FileManager

class DFWriterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.title("Distraction-Free Writer")
        self.configure(bg='#1e1e1e')
        
        # Standard wide-screen setup
        self.window_width = 1280
        self.window_height = 400
        self.center_window()
        self.setup_window_properties()

        self.current_frame = None
        
        # Bind global keyboard shortcuts at app level
        self.bind('<Control-s>', lambda e: self.handle_save())
        self.bind('<Control-o>', lambda e: self.handle_open())
        self.bind('<Control-b>', lambda e: self.handle_new_book())
        
        self.show_project_picker()

    def setup_window_properties(self):
        # Apply standard distraction-free attributes
        system = platform.system().lower()
        if system == 'windows':
            self.overrideredirect(True) # Borderless
            # Note: For development/debugging it might be better to have borders, but requirement is "appliance-like"
        elif system == 'linux':
            self.attributes('-type', 'dock') 

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def switch_frame(self, frame_class, *args, **kwargs):
        print(f"DEBUG: switch_frame called with {frame_class.__name__}")
        if self.current_frame:
            print(f"DEBUG: Destroying current frame: {type(self.current_frame).__name__}")
            self.current_frame.destroy()
        
        print(f"DEBUG: Creating new frame: {frame_class.__name__}")
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        print(f"DEBUG: New frame packed")
        # Force window update to ensure new frame is visible
        self.update_idletasks()
        self.update()
        # Ensure window is visible and on top
        self.deiconify()
        self.lift()
        self.focus_force()
        print(f"DEBUG: switch_frame completed")
        return self.current_frame

    def show_book_wizard(self):
        self.switch_frame(BookWizard, on_complete=self.on_book_created)

    def on_book_created(self, book_data):
        title = book_data["title"]
        genre = book_data["genre"]
        description = book_data["description"]
        goals = {
            "target": book_data["target_word_count"],
            "daily": book_data["daily_word_goal"]
        }
        
        new_path = self.file_manager.create_book(title, genre, description, goals)
        self.show_editor(new_path)

    def show_project_picker(self):
        print("DEBUG: show_project_picker called")
        print(f"DEBUG: current_frame before switch: {self.current_frame}")
        self.switch_frame(ProjectPicker, on_project_selected=self.show_editor)
        print(f"DEBUG: current_frame after switch: {self.current_frame}")
        # Ensure window is visible and on top
        self.deiconify()
        self.lift()
        self.focus_force()

    def show_editor(self, project_path):
        self.switch_frame(DFWriter, project_path=project_path)
    
    def handle_save(self):
        """Handle Ctrl+S shortcut"""
        if isinstance(self.current_frame, DFWriter):
            self.current_frame.logic.save_file()
    
    def handle_open(self):
        """Handle Ctrl+O shortcut"""
        if isinstance(self.current_frame, DFWriter):
            self.current_frame.logic.open_file()
    
    def handle_new_book(self):
        """Handle Ctrl+B shortcut"""
        if isinstance(self.current_frame, DFWriter):
            self.current_frame.logic.start_new_book_wizard()
        elif isinstance(self.current_frame, ProjectPicker):
            self.current_frame.start_new_book()

if __name__ == "__main__":
    app = DFWriterApp()
    app.mainloop()