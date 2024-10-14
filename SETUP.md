#!/bin/bash

# Update and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install Ghostwriter
sudo apt install -y ghostwriter

# Install LightDM and LXDE core
sudo apt install -y lightdm lxde-core

# Enable graphical target   
sudo systemctl set-default graphical.target

# Set up autologin
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf > /dev/null <<EOT
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOT

# Configure LightDM for autologin
sudo tee /etc/lightdm/lightdm.conf > /dev/null <<EOT
[Seat:*]
autologin-user=$USER
autologin-user-timeout=0
EOT

# Set up .xsession file for LXDE autostart
tee /home/$USER/.xsession > /dev/null <<EOT
exec startlxde
EOT
chmod +x /home/$USER/.xsession
chown $USER:$USER /home/$USER/.xsession

# Set up autostart for Ghostwriter
mkdir -p /home/$USER/.config/autostart
tee /home/$USER/.config/autostart/ghostwriter.desktop > /dev/null <<EOT
[Desktop Entry]
Type=Application
Name=Ghostwriter
Exec=ghostwriter
EOT
chown -R $USER:$USER /home/$USER/.config

# Remove this script so it doesn't run on subsequent boots
sudo rm /boot/firstboot.sh

# Reboot to apply changes
sudo reboot