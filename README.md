# MIDI-Player-GUI

## FedoraIOT (rpm-ostree)

On Client:<br/>
Enable autologin on default user:
```
sudo systemctl edit getty@tty1
```

Add the following lines:
```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin user --noclear %I $TERM
```
Close and exit, then reboot. Autologin should now be enabled.<br/><br/>

To install the main package:
```
sudo rpm-ostree install ./MIDI-Player-GUI-client
```
After installing restart system.

### Install pip packages
To install mido and python-rtmidi do:
```
pip install mido python-rtmidi
```

### Change splash screen

New theme is installed with rpm, set it explicitly with:
```
sudo plymouth-set-default-theme mpg-organ
```

Add necessary kernel arguments by:
```
sudo rpm-ostree initramfs --enable
```
and (for Raspberry Zero 2 W)
```
sudo rpm-ostree kargs --append="quiet splash console=tty1 initcall_blacklist=simpledrm_platform_driver_init" --delete=modprobe.blacklist=vc4
```
for x64 based systems (e.g. miniPC)
```
sudo rpm-ostree kargs --append="quiet splash"
```

### Autostart X-Server

Copy xinitrc file from source directory as normal user:
```
cat /opt/MIDI-Player-GUI/Config/xinitrc-client > $HOME/.xinitrc
```

Add startx to bashrc by:
```
cat /opt/MIDI-Player-GUI/Config/bashrc-client >> $HOME/.bashrc
```

Copy openbox custom theme files:
```
cp -rv /opt/MIDI-Player-GUI/Config/openbox $HOME/.config
```

Uncomment the startx-Midi function in .bashrc when ready.

Set static IP address:
```
mcli connection add con-name midi-static ifname enp1s0 type ethernet ip4 192.168.99.2/24
```



## Helpful sites
[MIDI note numbers and center frequencies](https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)<br/>
[Mido docs](https://mido.readthedocs.io/en/stable/intro.html)<br/>
[MIDECO user manual](https://www.midi-hardware.com/instrukcje/midecousman7.pdf)
[Doepfer MTC64 manual](https://doepfer.de/pdf/MTC64_ANL.PDF)

[LCD-Touch-Driver](https://github.com/goodtft/LCD-show)
