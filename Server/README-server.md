## FedoraIOT (rpm-ostree)

On Server:<br/>
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
sudo rpm-ostree install ./MIDI-Player-GUI-server
```
After installing restart system.

### Install pip packages
To install mido and python-rtmidi do:
```
pip install mido python-rtmidi
```

### Autostart X-Server

Copy xinitrc file from source directory as normal user:
```
cat /opt/MIDI-Player-GUI/Config/xinitrc-server > $HOME/.xinitrc
```

Add startx to bashrc by:
```
cat /opt/MIDI-Player-GUI/Config/bashrc-server >> $HOME/.bashrc
```

Uncomment the startx-Midi function in .bashrc when ready.

Set static IP address:
```
mcli connection add con-name midi-static ifname enp1s0 type ethernet ip4 192.168.99.2/24
```
