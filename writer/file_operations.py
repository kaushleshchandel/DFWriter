import os
import json
from datetime import datetime

class FileManager:
    def __init__(self, base_path="/home/pi/books"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def save_chapter(self, book_title, chapter_title, text):
        book_path = os.path.join(self.base_path, book_title)
        if not os.path.exists(book_path):
            os.makedirs(book_path)

        chapter_path = os.path.join(book_path, f"{chapter_title}.json")
        
        # Load existing data or create new structure
        if os.path.exists(chapter_path):
            with open(chapter_path, 'r') as f:
                chapter_data = json.load(f)
        else:
            chapter_data = {"versions": []}

        # Add new version
        new_version = {
            "timestamp": datetime.now().isoformat(),
            "text": text
        }
        chapter_data["versions"].append(new_version)

        # Save updated data
        with open(chapter_path, 'w') as f:
            json.dump(chapter_data, f, indent=2)

    def get_chapter(self, book_title, chapter_title, version=-1):
        chapter_path = os.path.join(self.base_path, book_title, f"{chapter_title}.json")
        
        if not os.path.exists(chapter_path):
            return None

        with open(chapter_path, 'r') as f:
            chapter_data = json.load(f)

        if version == -1:  # Latest version
            return chapter_data["versions"][-1]["text"]
        elif 0 <= version < len(chapter_data["versions"]):
            return chapter_data["versions"][version]["text"]
        else:
            return None

    def get_chapter_history(self, book_title, chapter_title):
        chapter_path = os.path.join(self.base_path, book_title, f"{chapter_title}.json")
        
        if not os.path.exists(chapter_path):
            return None

        with open(chapter_path, 'r') as f:
            chapter_data = json.load(f)

        return [{"version": i, "timestamp": v["timestamp"]} for i, v in enumerate(chapter_data["versions"])]

    def list_books(self):
        return [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]

    def list_chapters(self, book_title):
        book_path = os.path.join(self.base_path, book_title)
        if not os.path.isdir(book_path):
            return None
        return [f[:-5] for f in os.listdir(book_path) if f.endswith('.json')]