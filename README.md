# DFWriter
Distraction free writing tool for Raspberry pi



### Listener App
sudo apt update
sudo apt install python3-evdev -y

sudo apt-get install python3-tk


sudo nano /etc/systemd/system/keyboard-listener.service

[Unit]
Description=Keyboard Listener Service
After=multi-user.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/keyboard_listener.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload

sudo systemctl restart keyboard-listener.service