import tkinter as tk
from dfwriter import DFWriter

if __name__ == "__main__":
    root = tk.Tk()
    editor = DFWriter(root)
    root.mainloop()