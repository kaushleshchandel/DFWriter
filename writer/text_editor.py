import tkinter as tk
from tkinter import font, messagebox
from file_operations import open_file, save_file
from spellchecker import SpellChecker
import re

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor with Real-time Spell Checker")
        self.root.geometry("1280x400")

        self.spell = SpellChecker()
        
        self.setup_text_area()
        self.setup_menu()
        self.setup_toolbar()

    def setup_text_area(self):
        self.text_area = tk.Text(self.root, wrap="word", undo=True, height=15)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)
        
        default_font = font.nametofont(self.text_area.cget("font"))
        default_font.configure(size=14)
        self.text_area.configure(font=default_font)

        self.text_area.tag_configure("center", justify='center')
        self.text_area.tag_add("center", "1.0", "end")

        self.text_area.tag_configure("misspelled", foreground="red", underline=True)

        # Bind events for real-time spell checking
        self.text_area.bind("<space>", self.check_spelling_real_time)
        self.text_area.bind("<Return>", self.check_spelling_real_time)
        self.text_area.bind("<Tab>", self.check_spelling_real_time)
        self.text_area.bind("<KeyRelease>", self.check_spelling_real_time)

    def setup_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)

        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Check Spelling", command=self.check_spelling_full)

    def setup_toolbar(self):
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="top", fill="x")

        self.bold_button = tk.Button(self.toolbar, text="B", width=2, command=self.toggle_bold)
        self.bold_button.pack(side="left", padx=2, pady=2)

        self.italic_button = tk.Button(self.toolbar, text="I", width=2, command=self.toggle_italic)
        self.italic_button.pack(side="left", padx=2, pady=2)

        self.spell_check_button = tk.Button(self.toolbar, text="Full Spell Check", command=self.check_spelling_full)
        self.spell_check_button.pack(side="left", padx=2, pady=2)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.tag_add("center", "1.0", "end")

    def open_file(self):
        content = open_file()
        if content:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
            self.text_area.tag_add("center", "1.0", "end")
            self.check_spelling_full()

    def save_file(self):
        content = self.text_area.get(1.0, tk.END)
        save_file(content)

    def toggle_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
        self.text_area.tag_configure("bold", font=font.Font(weight="bold", size=14))

    def toggle_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
        self.text_area.tag_configure("italic", font=font.Font(slant="italic", size=14))

    def check_spelling_real_time(self, event):
        # Don't check spelling for special keys
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return

        index = self.text_area.index("insert")
        line, col = map(int, index.split("."))
        
        # Get the word before the cursor
        line_start = f"{line}.0"
        content = self.text_area.get(line_start, index)
        words = re.findall(r'\b\w+\b', content)
        
        if words:
            last_word = words[-1]
            if last_word not in self.spell:
                word_start = content.rindex(last_word)
                word_end = word_start + len(last_word)
                self.text_area.tag_add("misspelled", f"{line}.{word_start}", f"{line}.{word_end}")
            else:
                # Remove misspelled tag if the word is now correct
                self.text_area.tag_remove("misspelled", f"{line}.0", f"{line}.{col}")

        # Schedule the next check after a short delay
        self.root.after(100, self.check_previous_word)

    def check_previous_word(self):
        index = self.text_area.index("insert")
        line, col = map(int, index.split("."))
        
        # Get the word before the cursor
        line_start = f"{line}.0"
        content = self.text_area.get(line_start, index)
        words = re.findall(r'\b\w+\b', content)
        
        if words:
            last_word = words[-1]
            if last_word not in self.spell:
                word_start = content.rindex(last_word)
                word_end = word_start + len(last_word)
                self.text_area.tag_add("misspelled", f"{line}.{word_start}", f"{line}.{word_end}")
            else:
                # Remove misspelled tag if the word is now correct
                self.text_area.tag_remove("misspelled", f"{line}.0", f"{line}.{col}")


    def check_spelling_full(self):
        content = self.text_area.get("1.0", tk.END)
        words = re.findall(r'\b\w+\b', content)
        misspelled = self.spell.unknown(words)

        if not misspelled:
            messagebox.showinfo("Spell Check", "No misspelled words found!")
            return

        self.text_area.tag_remove("misspelled", "1.0", tk.END)

        for word in misspelled:
            start = "1.0"
            while True:
                start = self.text_area.search(r'\y' + re.escape(word) + r'\y', start, tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(word)}c"
                self.text_area.tag_add("misspelled", start, end)
                start = end

        self.show_correction_dialog(list(misspelled)[0])

    def show_correction_dialog(self, word):
        corrections = self.spell.candidates(word)
        dialog = tk.Toplevel(self.root)
        dialog.title("Spelling Correction")
        dialog.geometry("300x150")

        label = tk.Label(dialog, text=f"Suggestions for '{word}':")
        label.pack(pady=5)

        correction_var = tk.StringVar(dialog)
        correction_var.set(next(iter(corrections)))  # Set the first correction as default

        correction_menu = tk.OptionMenu(dialog, correction_var, *corrections)
        correction_menu.pack(pady=5)

        def apply_correction():
            new_word = correction_var.get()
            start = self.text_area.index("insert-1c wordstart")
            end = self.text_area.index("insert-1c wordend")
            self.text_area.delete(start, end)
            self.text_area.insert(start, new_word)
            self.text_area.tag_remove("misspelled", start, f"{start}+{len(new_word)}c")
            dialog.destroy()
            self.check_spelling_full()  # Continue checking for other misspelled words

        apply_button = tk.Button(dialog, text="Apply Correction", command=apply_correction)
        apply_button.pack(pady=5)

        ignore_button = tk.Button(dialog, text="Ignore", command=lambda: [dialog.destroy(), self.check_spelling_full()])
        ignore_button.pack(pady=5)