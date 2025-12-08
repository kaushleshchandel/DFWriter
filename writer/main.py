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
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
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
        self.switch_frame(ProjectPicker, on_project_selected=self.show_editor)

    def show_editor(self, project_path):
        self.switch_frame(DFWriter, project_path=project_path)

if __name__ == "__main__":
    app = DFWriterApp()
    app.mainloop()