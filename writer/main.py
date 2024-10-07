import tkinter as tk
from text_editor import TextEditor

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()