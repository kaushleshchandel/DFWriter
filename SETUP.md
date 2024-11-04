
# Update and upgrade the system

```
sudo apt update
sudo apt upgrade -y
```


## Setup GUI

```
sudo apt install xserver-xorg x11-xserver-utils xinit openbox
sudo apt install python3-tk
```

## Create a simple script to start your application. Let's make it at

```
sudo nano /home/pi/autorun.sh
```

Add following to the bash file

```
#!/bin/bash
export DISPLAY=:0
python3 /home/pi/app/main.py
```


Make Script executable

```
sudo chmod +x /home/pi/autorun.sh
```



Create an Openbox autostart file at 

```
sudo nano /etc/xdg/openbox/autostart
```


```
#!/bin/bash
## Disable screen blanking
xset s off
xset -dpms
xset s noblank

## Start your application
/home/pi/autorun.sh &
```


## Create a service file at 

sudo nano /etc/systemd/system/startx.service

```

[Unit]
Description=Start X Server
After=multi-user.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/startx -- -nocursor
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


Enable service

```
sudo systemctl enable startx.service
sudo systemctl start startx.service
```


Create the DFWRiter files inside the app folder

sudo nano dfwriter.py

sudo nano file_operations.py

sudo nano logic.py

sudo nano main.py

sudo nano update.py