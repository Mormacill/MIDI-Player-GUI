#!/bin/bash

#Path to midi.py
EXPATH=/opt/MIDI-Player-GUI

#Default path for USB-Mount on Raspberry Pi OS
#cd /media/user

#Infinite loop for auto restart if app closed or crashed
while :
  do
    python $EXPATH/Source/midi-receive.py
  done
