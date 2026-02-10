# MIDI-Player-GUI

## FedoraIOT (rpm-ostree)

On Client:<br/>
Enable autologin on default user:<br/>
`sudo systemctl edit getty@tty1`<br/>

Add the following lines:
```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin user --noclear %I $TERM
```
Close and exit, then reboot. Autologin should now be enabled.<br/><br/>

To install the main package:
`dnf install MIDI-Player-GUI-client`<br/>
After installing restart system.

### Install pip packages
To install mido and python-rtmidi do:<br/>
`pip install mido python-rtmidi`

### Change splash screen

New theme is installed with rpm, set it explicitly with:<br/>
`plymouth-set-default-theme mpg-organ`

Add necessarykernel arguments by:<br/>
`sudo rpm-ostree initramfs --enable`<br/>
and<br/>
`sudo rpm-ostree kargs --append="quiet splash"`

### Autostart X-Server

Copy xinitrc file from source directory as normal user:<br/>
`cat /opt/MIDI-Player-GUI/Config/xinitrc-client > $PWD/.xinitrc`

Add startx to bashrc by:<br/>
`cat /opt/MIDI-Player-GUI/Config/bashrc-client >> $PWD/.bashrc`<br/>
Uncomment the startx-Midi function when ready.



## Helpful sites
[MIDI note numbers and center frequencies](https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)<br/>
[Mido docs](https://mido.readthedocs.io/en/stable/intro.html)<br/>
[MIDECO user manual](https://www.midi-hardware.com/instrukcje/midecousman7.pdf)
[Doepfer MTC64 manual](https://doepfer.de/pdf/MTC64_ANL.PDF)

[LCD-Touch-Driver](https://github.com/goodtft/LCD-show)
