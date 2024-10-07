import os
import subprocess

DEBUG = True
POPUP_DURATION = 3000

# Dictionary mapping key combinations to functions and descriptions
APP_LAUNCHES = {
    ('KEY_COMPOSE', 'KEY_W'): ("env DISPLAY=:0 python3 /home/pi/app/DFWriter/main.py", "Launching DF Writer"),
    ('KEY_COMPOSE', 'KEY_H'): ("env DISPLAY=:0 python3 /home/pi/app/DFWriter/main.py", "Launching Home"),
    # Add more combinations as needed
}

# Special functions
def function_reboot():
    subprocess.run(["sudo", "reboot"])

def function_shutdown():
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def function_sleep():
    subprocess.run(["sudo", "systemctl", "suspend"])

# Dictionary mapping key combinations to special functions
SPECIAL_FUNCTIONS = {
    ('KEY_COMPOSE', 'KEY_R'): (function_reboot, "Executing Reboot"),
    ('KEY_COMPOSE', 'KEY_S'): (function_shutdown, "Executing Shutdown"),
    ('KEY_COMPOSE', 'KEY_L'): (function_sleep, "Putting system to sleep"),
    # Add more special functions as needed
}