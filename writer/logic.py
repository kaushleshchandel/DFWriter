import tkinter as tk
from tkinter import filedialog
import re
from book_wizard import BookWizard
from file_operations import FileManager
from wide_dialogs import WideScreenFileDialog, WideScreenMessageDialog

class DistractionFreeEditorLogic:
    def __init__(self, dfwriter, project_path=None):
        self.dfwriter = dfwriter
        self.file_manager = FileManager()
        self.current_book_path = project_path
        self.current_chapter = "Chapter_01"
        self.current_page = 1
        self.auto_save_enabled = True
        self.auto_save_delay = 2000  # 2 seconds in milliseconds
        
        if self.current_book_path:
            self.load_project_metadata()
            # Delay loading page content until UI is ready
            # Will be called after layout is created

    def load_project_metadata(self):
        # Load metadata and update UI
        metadata = self.file_manager.get_metadata(self.current_book_path)
        if metadata:
            title = metadata.get("title", "Untitled")
            genre = metadata.get("genre", "General")
            
            # Get current position
            self.current_chapter, self.current_page = self.file_manager.get_current_position(self.current_book_path)
            
            # Update UI
            self.update_breadcrumb(title, self.current_chapter, self.current_page)
            self.dfwriter.update_custom(genre, "Genre")
    
    def load_current_page(self):
        """Load the current page content into the editor."""
        if not self.current_book_path:
            return
        
        content = self.file_manager.load_page(self.current_book_path, self.current_chapter, self.current_page)
        if content:
            self.dfwriter.text_widget.delete(1.0, tk.END)
            self.dfwriter.text_widget.insert(tk.END, content)
            self.update_text_color()
        else:
            # New page, clear editor
            self.dfwriter.text_widget.delete(1.0, tk.END)
            self.update_text_color()
    
    def calculate_total_words(self):
        """Calculate total words across all chapters and pages in the book"""
        if not self.current_book_path:
            return 0
        
        total_words = 0
        chapters = self.file_manager.list_chapters(self.current_book_path)
        
        for chapter in chapters:
            pages = self.file_manager.list_pages(self.current_book_path, chapter)
            for page_num in pages:
                content = self.file_manager.load_page(self.current_book_path, chapter, page_num)
                if content:
                    words = len(content.split())
                    total_words += words
        
        return total_words
    
    def update_breadcrumb(self, title, chapter, page):
        """Update breadcrumb display."""
        # Format chapter name nicely (Chapter_01 -> Chapter 1)
        chapter_display = chapter.replace("_", " ")
        if chapter_display.startswith("Chapter "):
            try:
                num = int(chapter_display.split()[1])
                chapter_display = f"Chapter {num}"
            except (ValueError, IndexError):
                pass
        
        self.dfwriter.update_breadcrumb(title, chapter_display, page)

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
        
        # Update word and page counts
        self.update_statistics()
        
        # Schedule auto-save
        if self.auto_save_enabled and self.current_book_path:
            self.schedule_auto_save()
    
    def schedule_auto_save(self):
        """Schedule an auto-save after a delay."""
        # Cancel any pending auto-save
        if hasattr(self, 'auto_save_job'):
            self.dfwriter.after_cancel(self.auto_save_job)
        
        # Schedule new auto-save
        self.auto_save_job = self.dfwriter.after(self.auto_save_delay, self.auto_save_page)
    
    def auto_save_page(self):
        """Automatically save the current page."""
        if not self.current_book_path:
            return
        
        content = self.dfwriter.text_widget.get(1.0, tk.END).rstrip('\n')
        self.file_manager.save_page(self.current_book_path, self.current_chapter, self.current_page, content)
        self.file_manager.update_current_position(self.current_book_path, self.current_chapter, self.current_page)
    
    def update_statistics(self):
        """Update word count and page count statistics"""
        content = self.dfwriter.text_widget.get(1.0, tk.END).rstrip('\n')
        
        # Count words (split by whitespace)
        words = len(content.split()) if content.strip() else 0
        self.dfwriter.update_words(words)
        
        # Estimate pages (assuming ~250 words per page)
        pages = max(1, (words // 250) + (1 if words % 250 > 0 else 0))
        self.dfwriter.update_pages(pages)
        
        # Update total book statistics if we have a book
        if self.current_book_path:
            total_words = self.calculate_total_words()
            self.dfwriter.update_custom(f"{total_words:,}", "Total Words")

    def new_file(self):
        """Clear current page (deprecated - use new_page instead)"""
        # This is now handled by new_page() which works within book structure
        if self.current_book_path:
            self.new_page()
        else:
            self.dfwriter.text_widget.delete(1.0, tk.END)
            self.update_text_color()

    def start_new_book_wizard(self):
        # Access the app instance (root window) and use its frame switching mechanism
        app = self.dfwriter.master
        if hasattr(app, 'show_book_wizard'):
            app.show_book_wizard()
        else:
            # Fallback: create BookWizard directly (shouldn't happen in normal flow)
            BookWizard(self.dfwriter.master, self.on_book_created)

    def on_book_created(self, book_data):
        title = book_data["title"]
        genre = book_data["genre"]
        description = book_data["description"]
        goals = {
            "target": book_data["target_word_count"],
            "daily": book_data["daily_word_goal"]
        }
        
        self.current_book_path = self.file_manager.create_book(title, genre, description, goals)
        
        # Reset editor for the new book
        self.new_file()
        
        # Update UI info (Assuming DFWriter has these methods/vars)
        self.dfwriter.update_breadcrumb(title, "Chapter 1", 1) # Placeholder chapter
        self.dfwriter.update_custom(genre, "Genre")
        
        print(f"Book created at: {self.current_book_path}") # Debug

    def open_file(self):
        """Open a page from a book using book navigator"""
        from book_navigator import BookNavigator
        
        # If we're already in a book, pass the current book path to skip book selection
        result = BookNavigator.show(self.dfwriter.master, mode='open', 
                                   current_book_path=self.current_book_path)
        if result:
            book_path = result['book_path']
            chapter = result['chapter']
            page = result['page']
            
            # Load the selected page
            content = self.file_manager.load_page(book_path, chapter, page)
            if content:
                # Update current position
                self.current_book_path = book_path
                self.current_chapter = chapter
                self.current_page = page
                
                # Load content
                self.dfwriter.text_widget.delete(1.0, tk.END)
                self.dfwriter.text_widget.insert(tk.END, content)
                self.update_text_color()
                
                # Update metadata and UI
                self.file_manager.update_current_position(book_path, chapter, page)
                self.load_project_metadata()
            else:
                WideScreenMessageDialog.showerror(
                    self.dfwriter.master,
                    title="Error",
                    message="Failed to load page"
                )

    def save_file(self):
        """Save current page to book structure. If no book is open, show message."""
        if not self.current_book_path:
            WideScreenMessageDialog.showwarning(
                self.dfwriter.master,
                title="No Book Open",
                message="Please open or create a book first. Use 'Start Book' to create a new book."
            )
            return
        
        # Save to book structure
        content = self.dfwriter.text_widget.get(1.0, tk.END).rstrip('\n')
        self.file_manager.save_page(self.current_book_path, self.current_chapter, self.current_page, content)
        self.file_manager.update_current_position(self.current_book_path, self.current_chapter, self.current_page)
        
        # Show brief confirmation (optional - can be removed for less distraction)
        # WideScreenMessageDialog.showinfo(
        #     self.dfwriter.master,
        #     title="Saved",
        #     message=f"Page {self.current_page} saved"
        # )
    
    def new_page(self):
        """Create a new page in the current chapter."""
        if not self.current_book_path:
            WideScreenMessageDialog.showwarning(
                self.dfwriter.master,
                title="No Book Open",
                message="Please open or create a book first."
            )
            return
        
        # Save current page first
        content = self.dfwriter.text_widget.get(1.0, tk.END).rstrip('\n')
        if content.strip():
            self.file_manager.save_page(self.current_book_path, self.current_chapter, self.current_page, content)
        
        # Get next page number
        self.current_page = self.file_manager.get_next_page_number(self.current_book_path, self.current_chapter)
        
        # Clear editor for new page
        self.dfwriter.text_widget.delete(1.0, tk.END)
        self.update_text_color()
        
        # Update metadata and UI
        self.file_manager.update_current_position(self.current_book_path, self.current_chapter, self.current_page)
        metadata = self.file_manager.get_metadata(self.current_book_path)
        if metadata:
            self.update_breadcrumb(metadata.get("title", "Untitled"), self.current_chapter, self.current_page)
    
    def new_chapter(self):
        """Create a new chapter with custom name."""
        if not self.current_book_path:
            WideScreenMessageDialog.showwarning(
                self.dfwriter.master,
                title="No Book Open",
                message="Please open or create a book first."
            )
            return
        
        # Ask for chapter name
        from chapter_dialog import ChapterNameDialog
        chapter_name = ChapterNameDialog.ask_chapter_name(self.dfwriter.master)
        
        if not chapter_name:
            return  # User cancelled
        
        # Save current page first
        content = self.dfwriter.text_widget.get(1.0, tk.END).rstrip('\n')
        if content.strip():
            self.file_manager.save_page(self.current_book_path, self.current_chapter, self.current_page, content)
        
        # Create new chapter with custom name
        self.current_chapter = chapter_name
        self.file_manager.create_chapter(self.current_book_path, self.current_chapter)
        self.current_page = 1
        
        # Clear editor for new chapter
        self.dfwriter.text_widget.delete(1.0, tk.END)
        self.update_text_color()
        
        # Update metadata and UI
        self.file_manager.update_current_position(self.current_book_path, self.current_chapter, self.current_page)
        metadata = self.file_manager.get_metadata(self.current_book_path)
        if metadata:
            self.update_breadcrumb(metadata.get("title", "Untitled"), self.current_chapter, self.current_page)
