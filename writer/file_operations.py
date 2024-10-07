from tkinter import filedialog

def open_file():
    file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file:
        content = file.read()
        file.close()
        return content
    return None

def save_file(content):
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file:
        file.write(content)
        file.close()