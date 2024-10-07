import tkinter as tk
from tkinter import ttk
import os

def reboot_system():
    os.system('sudo reboot')

def close_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Raspberry Pi Test App")
root.geometry("300x200")

# Make the window fullscreen
root.attributes('-fullscreen', True)

# Create and pack a text box
text_box = ttk.Entry(root)
text_box.pack(pady=20)

# Create and pack a reboot button
reboot_button = ttk.Button(root, text="Reboot", command=reboot_system)
reboot_button.pack(pady=10)

# Create and pack a close button
close_button = ttk.Button(root, text="Close App", command=close_app)
close_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()