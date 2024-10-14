import tkinter as tk
from dfwriter import DFWriter

if __name__ == "__main__":
    root = tk.Tk()
    app = DFWriter(root)
    
    # Example usage of update functions
    app.update_pages(5)
    app.update_words(1000)
    app.update_custom(50, "Characters")
    
    root.mainloop()