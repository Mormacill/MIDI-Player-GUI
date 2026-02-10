# MIDI-Player-GUI

## FedoraIOT (rpm-ostree)

On Client:
`dnf install MIDI-Player-GUI-client`

### Change splash screen

New theme is installed with rpm, set it explicitly with:
`plymouth-set-default-theme mpg-organ`

Add necessarykernel arguments by:
`sudo rpm-ostree initramfs --enable`
and
`sudo rpm-ostree kargs --append="quiet splash"`

### Autostart X-Server

Copy xinitrc file from source directory as normal user:
`cat /opt/MIDI-Player-GUI/Config/xinitrc > $PWD/.xinitrc`

Add startx to bashrc by:
`cat /opt/MIDI-Player-GUI/Config/bashrc >> $PWD/.bashrc`
Uncomment the startx-Midi function when ready.



## Helpful sites
[MIDI note numbers and center frequencies](https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)<br/>
[Mido docs](https://mido.readthedocs.io/en/stable/intro.html)<br/>
[MIDECO user manual](https://www.midi-hardware.com/instrukcje/midecousman7.pdf)
[Doepfer MTC64 manual](https://doepfer.de/pdf/MTC64_ANL.PDF)

[LCD-Touch-Driver](https://github.com/goodtft/LCD-show)
