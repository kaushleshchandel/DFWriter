import os
import json
from datetime import datetime

class FileManager:
    def __init__(self, base_path=None):
        if base_path is None:
            # Get the app root directory (parent of writer folder)
            # This file is in writer/, so we go up one level to get app root
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            app_root = os.path.dirname(current_file_dir)  # Go up from writer/ to app root
            self.base_path = os.path.join(app_root, "books")
        else:
            self.base_path = base_path
            
        # Create books directory if it doesn't exist
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def create_book(self, title, genre, description, goals):
        """Creates a new book folder with proper structure:
        BookFolder/
          - metadata.json
          - chapters/
            - Chapter_01/
              - page_001.txt
              - page_002.txt
              - ...
        """
        # Sanitize title for filesystem
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        book_path = os.path.join(self.base_path, safe_title)
        
        if not os.path.exists(book_path):
            os.makedirs(book_path)
            
        # Create chapters directory
        chapters_path = os.path.join(book_path, "chapters")
        if not os.path.exists(chapters_path):
            os.makedirs(chapters_path)
        
        # Create first chapter
        first_chapter = "Chapter_01"
        chapter_path = os.path.join(chapters_path, first_chapter)
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)
            
        metadata = {
            "title": title,
            "genre": genre,
            "description": description,
            "goals": goals,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "current_chapter": first_chapter,
            "current_page": 1
        }
        
        self.save_metadata(book_path, metadata)
        return book_path

    def save_metadata(self, book_path, metadata):
        """Saves book metadata to a JSON file."""
        metadata_path = os.path.join(book_path, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

    def save_page(self, book_path, chapter_name, page_number, content):
        """Save a page within a chapter. Creates chapter folder if it doesn't exist."""
        chapters_path = os.path.join(book_path, "chapters")
        chapter_path = os.path.join(chapters_path, chapter_name)
        
        # Create chapter folder if it doesn't exist
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)
        
        # Format page number as page_XXX.txt
        page_filename = f"page_{page_number:03d}.txt"
        page_path = os.path.join(chapter_path, page_filename)
        
        # Save page content
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update metadata last_modified
        metadata = self.get_metadata(book_path)
        if metadata:
            metadata["last_modified"] = datetime.now().isoformat()
            self.save_metadata(book_path, metadata)
    
    def load_page(self, book_path, chapter_name, page_number):
        """Load a specific page from a chapter."""
        chapters_path = os.path.join(book_path, "chapters")
        chapter_path = os.path.join(chapters_path, chapter_name)
        page_filename = f"page_{page_number:03d}.txt"
        page_path = os.path.join(chapter_path, page_filename)
        
        if not os.path.exists(page_path):
            return None
        
        with open(page_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_metadata(self, book_path):
        """Load book metadata."""
        metadata_path = os.path.join(book_path, "metadata.json")
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_current_position(self, book_path, chapter_name, page_number):
        """Update the current chapter and page in metadata."""
        metadata = self.get_metadata(book_path)
        if metadata:
            metadata["current_chapter"] = chapter_name
            metadata["current_page"] = page_number
            metadata["last_modified"] = datetime.now().isoformat()
            self.save_metadata(book_path, metadata)
    
    def list_chapters(self, book_path):
        """List all chapters in a book."""
        chapters_path = os.path.join(book_path, "chapters")
        if not os.path.exists(chapters_path):
            return []
        
        chapters = []
        for item in os.listdir(chapters_path):
            chapter_path = os.path.join(chapters_path, item)
            if os.path.isdir(chapter_path):
                chapters.append(item)
        
        # Sort chapters naturally (Chapter_01, Chapter_02, etc.)
        chapters.sort()
        return chapters
    
    def list_pages(self, book_path, chapter_name):
        """List all pages in a chapter."""
        chapters_path = os.path.join(book_path, "chapters")
        chapter_path = os.path.join(chapters_path, chapter_name)
        
        if not os.path.exists(chapter_path):
            return []
        
        pages = []
        for item in os.listdir(chapter_path):
            if item.startswith("page_") and item.endswith(".txt"):
                # Extract page number from filename
                try:
                    page_num = int(item[5:8])  # Extract from "page_XXX.txt"
                    pages.append(page_num)
                except ValueError:
                    continue
        
        pages.sort()
        return pages
    
    def get_next_page_number(self, book_path, chapter_name):
        """Get the next available page number for a chapter."""
        pages = self.list_pages(book_path, chapter_name)
        if not pages:
            return 1
        return max(pages) + 1
    
    def get_current_position(self, book_path):
        """Get current chapter and page from metadata."""
        metadata = self.get_metadata(book_path)
        if metadata:
            return metadata.get("current_chapter", "Chapter_01"), metadata.get("current_page", 1)
        return "Chapter_01", 1

    def list_books(self):
        return [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]

    def create_chapter(self, book_path, chapter_name):
        """Create a new chapter folder."""
        chapters_path = os.path.join(book_path, "chapters")
        chapter_path = os.path.join(chapters_path, chapter_name)
        
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)
        
        return chapter_path
    
    def get_next_chapter_name(self, book_path):
        """Get the next available chapter name (e.g., Chapter_02)."""
        chapters = self.list_chapters(book_path)
        if not chapters:
            return "Chapter_01"
        
        # Find the highest chapter number
        max_num = 0
        for chapter in chapters:
            if chapter.startswith("Chapter_"):
                try:
                    num = int(chapter.split("_")[1])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    continue
        
        return f"Chapter_{max_num + 1:02d}"
    
    def get_book_statistics(self, book_path):
        """Get comprehensive statistics for a book."""
        metadata = self.get_metadata(book_path)
        if not metadata:
            return None
        
        # Calculate total words
        total_words = 0
        total_pages = 0
        chapters = self.list_chapters(book_path)
        
        for chapter in chapters:
            pages = self.list_pages(book_path, chapter)
            total_pages += len(pages)
            for page_num in pages:
                content = self.load_page(book_path, chapter, page_num)
                if content:
                    words = len(content.split())
                    total_words += words
        
        # Get target word count
        goals = metadata.get("goals", {})
        target_words = int(goals.get("target", 50000))
        
        # Calculate progress percentage
        progress = min(100, int((total_words / target_words) * 100)) if target_words > 0 else 0
        
        return {
            "title": metadata.get("title", "Untitled"),
            "genre": metadata.get("genre", "Unknown"),
            "total_words": total_words,
            "target_words": target_words,
            "total_pages": total_pages,
            "total_chapters": len(chapters),
            "progress": progress,
            "last_modified": metadata.get("last_modified", ""),
            "created_at": metadata.get("created_at", "")
        }