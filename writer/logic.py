import tkinter as tk
from tkinter import filedialog
import re

class DistractionFreeEditorLogic:
    def __init__(self, dfwriter):
        self.dfwriter = dfwriter

    def interpolate_color(self, color1, color2, t):
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 * (1-t) + r2 * t)
        g = int(g1 * (1-t) + g2 * t)
        b = int(b1 * (1-t) + b2 * t)
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_text_color(self, event=None):
        content = self.dfwriter.text_widget.get("1.0", tk.END)
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        # Remove all existing tags
        for i in range(5):
            self.dfwriter.text_widget.tag_remove(f"color_{i}", "1.0", tk.END)
        
        start = "1.0"
        for i, sentence in enumerate(sentences):
            if i == len(sentences) - 1:  # Current sentence
                self.dfwriter.text_widget.tag_add("color_0", start, tk.END)
            else:
                end = self.dfwriter.text_widget.search(re.escape(sentence), start, stopindex=tk.END)
                if end:
                    end = f"{end}+{len(sentence)}c"
                    color_index = min(4, i)  # Cap at 4 to avoid creating too many shades
                    self.dfwriter.text_widget.tag_add(f"color_{color_index}", start, end)
                    start = end

    def new_file(self):
        self.dfwriter.text_widget.delete(1.0, tk.END)
        self.update_text_color()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.dfwriter.text_widget.delete(1.0, tk.END)
                self.dfwriter.text_widget.insert(tk.END, content)
            self.update_text_color()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.dfwriter.text_widget.get(1.0, tk.END)
                file.write(content)