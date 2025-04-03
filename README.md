# MIDI-Player-GUI

## debian bzw. raspian

`apt install python3-tk python3-mido python3-rtmidi`

## Change splash screen

replace splash.png file in
`/usr/share/plymouth/themes/pix/`

## add bash script to autostart

open
`/etc/xdg/lxsession/LXDE-pi/autostart`
and add
`@lxterminal -e bash /home/user/Documents/MIDI-Player-GUI/midi-start.sh`
