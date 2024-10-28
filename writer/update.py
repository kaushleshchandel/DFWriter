# update_checker.py
import json
import os
import sys
import requests
import tkinter as tk
from tkinter import messagebox
import subprocess
import logging
from pathlib import Path

class UpdateManager:
    def __init__(self):
        self.config = {
            'update_url': 'http://your-server.com/updates',
            'version_file': 'version.json',
            'app_dir': Path('/home/pi/myapp'),
            'main_app': 'main_app.py'
        }
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='/var/log/app-updater.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def check_for_updates(self):
        try:
            # Get current version
            current_version = self.get_current_version()
            
            # Fetch version info from server
            response = requests.get(f"{self.config['update_url']}/{self.config['version_file']}")
            server_info = response.json()
            
            if server_info['version'] > current_version:
                return server_info
            return None
        except Exception as e:
            logging.error(f"Error checking for updates: {str(e)}")
            return None

    def get_current_version(self):
        version_file = self.config['app_dir'] / 'version.json'
        if version_file.exists():
            with open(version_file) as f:
                return json.load(f)['version']
        return "0.0.0"

    def download_update(self, update_info):
        try:
            # Create temp directory for downloads
            temp_dir = self.config['app_dir'] / 'temp'
            temp_dir.mkdir(exist_ok=True)

            # Download each file listed in the update
            for file_info in update_info['files']:
                url = f"{self.config['update_url']}/{file_info['path']}"
                local_path = temp_dir / file_info['path']
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                response = requests.get(url)
                with open(local_path, 'wb') as f:
                    f.write(response.content)

            # Move files to proper locations
            for file_info in update_info['files']:
                src = temp_dir / file_info['path']
                dst = self.config['app_dir'] / file_info['path']
                dst.parent.mkdir(parents=True, exist_ok=True)
                src.replace(dst)

            # Clean up temp directory
            for item in temp_dir.glob('**/*'):
                if item.is_file():
                    item.unlink()
            temp_dir.rmdir()

            # Save new version info
            with open(self.config['app_dir'] / 'version.json', 'w') as f:
                json.dump({'version': update_info['version']}, f)

            return True
        except Exception as e:
            logging.error(f"Error downloading update: {str(e)}")
            return False

    def show_update_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askyesno(
            "Software Update",
            "A new software update is available. Would you like to update now?"
        )
        
        root.destroy()
        return result

    def start_app(self):
        app_path = self.config['app_dir'] / self.config['main_app']
        if app_path.exists():
            subprocess.Popen([sys.executable, str(app_path)])
        else:
            logging.error("Main application not found!")

    def run(self):
        logging.info("Starting update check...")
        update_info = self.check_for_updates()
        
        if update_info:
            logging.info(f"Update found: version {update_info['version']}")
            if self.show_update_dialog():
                if self.download_update(update_info):
                    logging.info("Update successfully installed")
                    messagebox.showinfo("Update Complete", 
                                      "The software has been updated successfully.")
                else:
                    logging.error("Update failed")
                    messagebox.showerror("Update Failed", 
                                       "Failed to install the update. Please try again later.")
        
        self.start_app()

if __name__ == "__main__":
    manager = UpdateManager()
    manager.run()