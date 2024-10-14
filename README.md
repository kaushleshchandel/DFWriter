# DFWriter
Distraction free writing tool for Raspberry pi


## SETUP Raspberry pi

Install Raspberry pi lite OS. Before Inserting the SD card, customize the Boot Settings.

Add these at the end for Display

```
hdmi_force_hotplug=1
hdmi_ignore_edid=0xa5000080
hdmi_group=2
hdmi_mode=87
hdmi_timings=1280 0 64 2 18 400 0 10 3 42 0 0 0 60 0 37330000 3
hdmi_drive=1
```

Create firstboot.sh file in the root folder of SD card


To make this script run on first boot, modify the cmdline.txt file in the boot partition. Add this to the end of the existing line:

init=/bin/bash -c "mount -t proc proc /proc; mount -t sysfs sys /sys; mount /boot; source /boot/firstboot.sh"


### Install light Desktop


### Customize Raspberry pi


### Enable Network drive


### Install custom theme for startup

Install Plymouth

```
sudo apt install plymouth plymouth-themes
```

Configure the kernel to use Plymouth. Edit the kernel command line

```
sudo nano /boot/firmware/cmdline.txt
```

Add these parameters to end of the line

```
quiet splash plymouth.ignore-serial-consoles logo.nologo
```

Enable Plymouth service

```
sudo systemctl enable plymouth
```

Now, let's create a custom splash screen. You'll need an image file (PNG format is recommended). Let's assume you have an image named splash.png. Copy it to the Plymouth themes directory:
Copysudo cp /path/to/your/splash.png /usr/share/plymouth/themes/

Create a new Plymouth theme:
Copysudo nano /usr/share/plymouth/themes/custom-splash/custom-splash.plymouth
Add the following content:
Copy[Plymouth Theme]
Name=Custom Splash
Description=A custom splash screen
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/custom-splash
ScriptFile=/usr/share/plymouth/themes/custom-splash/custom-splash.script

Create the script file:
Copysudo nano /usr/share/plymouth/themes/custom-splash/custom-splash.script
Add the following content:
Copywallpaper_image = Image("splash.png");
screen_width = Window.GetWidth();
screen_height = Window.GetHeight();
resized_wallpaper_image = wallpaper_image.Scale(screen_width, screen_height);
wallpaper_sprite = Sprite(resized_wallpaper_image);
wallpaper_sprite.SetZ(-100);

Set your custom theme as the default:
Copysudo plymouth-set-default-theme -R custom-splash

Update the initramfs:
Copysudo update-initramfs -u

Reboot your Raspberry Pi:
Copysudo reboot