import evdev
from evdev import ecodes, categorize
import asyncio
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import logging
import os
from config import APP_LAUNCHES, SPECIAL_FUNCTIONS, DEBUG, POPUP_DURATION

# Set up logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_popup(message):
    def show_popup():
        popup = tk.Tk()
        popup.wm_title("Action Triggered")
        popup.geometry("300x100")
        label = ttk.Label(popup, text=message, font=("TkDefaultFont", 12))
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.after(POPUP_DURATION, popup.destroy)
        popup.mainloop()

    popup_thread = threading.Thread(target=show_popup)
    popup_thread.start()

class KeyTracker:
    def __init__(self):
        self.pressed_keys = set()
        self.compose_pressed = False

    def on_event(self, event):
        logging.debug(f"Received event: {event}")
        
        if event.type == evdev.ecodes.EV_KEY:
            key_event = categorize(event)
            key_name = key_event.keycode
            if isinstance(key_name, list):
                key_name = key_name[0]

            if event.value == 1:  # Key pressed
                logging.info(f"Key pressed: {key_name}")
                self.pressed_keys.add(key_name)
                if key_name == 'KEY_COMPOSE':
                    self.compose_pressed = True
            elif event.value == 0:  # Key released
                logging.info(f"Key released: {key_name}")
                self.pressed_keys.discard(key_name)
                if key_name == 'KEY_COMPOSE':
                    self.compose_pressed = False
            elif event.value == 2:  # Key held
                logging.debug(f"Key held: {key_name}")

            self.check_combinations()

    def check_combinations(self):
        if self.compose_pressed:
            for combo, (action, description) in {**APP_LAUNCHES, **SPECIAL_FUNCTIONS}.items():
                if all(key in self.pressed_keys for key in combo):
                    logging.info(f"Combination detected: {combo}")
                    if isinstance(action, str):
                        subprocess.Popen(action, shell=True)
                        logging.info(f"Launching: {action}")
                    else:
                        action()
                        logging.info(f"Executing function: {action.__name__}")
                    create_popup(description)

async def handle_events(device, key_tracker):
    logging.info(f"Starting event loop for device: {device.path}")
    try:
        async for event in device.async_read_loop():
            key_tracker.on_event(event)
    except Exception as e:
        logging.error(f"Error reading from device {device.path}: {str(e)}")

async def main():
    if os.geteuid() != 0:
        logging.error("This script must be run with sudo privileges.")
        return

    key_tracker = KeyTracker()
    
    try:
        device = evdev.InputDevice('/dev/input/event0')
        logging.info(f"Using input device: {device.path}, {device.name}")
        logging.info(f"Device capabilities: {device.capabilities(verbose=True)}")
        
        await handle_events(device, key_tracker)
    except Exception as e:
        logging.error(f"Error setting up device: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())