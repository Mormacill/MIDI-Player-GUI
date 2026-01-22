# MIDI-Player-GUI

## debian bzw. raspian

`apt install python3-tk python3-mido python3-rtmidi`

## Change splash screen

replace splash.png file in
`/usr/share/plymouth/themes/pix/`

## Add bash script to autostart

open
`/etc/xdg/lxsession/LXDE-pi/autostart`
and add
`@lxterminal -e bash /home/user/Documents/MIDI-Player-GUI/midi-start.sh`

## Helpful sites
[MIDI note numbers and center frequencies](https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)
[Mido docs](https://mido.readthedocs.io/en/stable/intro.html)
[MIDECO user manual](https://www.midi-hardware.com/instrukcje/midecousman7.pdf)
