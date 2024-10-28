#!/bin/bash

# Update and upgrade the system
sudo apt update
sudo apt upgrade -y


# Setup GUI
 
sudo apt install xserver-xorg xserver-xorg-core -y
sudo apt install openbox obconf -y

sudo apt install python3-tk tint2 nitrogen pcmanfm -y

mkdir -p ~/.config/openbox
cp /etc/xdg/openbox/* ~/.config/openbox/


nano ~/.config/openbox/autostart

Add these lines

```
# Launch panel
tint2 &

# Set background to black (optional)
xsetroot -solid black &

# File manager daemon (optional)
pcmanfm --desktop &
```

echo "exec openbox-session" > ~/.xinitrc


 