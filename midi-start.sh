#!/bin/bash

#Path to midi.py
EXPATH=/home/user/Documents/MIDI-Player-GUI

#Default path for USB-Mount on Raspberry Pi OS
cd /media/user

#Give current IP if connected to Wifi
ifconfig | grep inet\

#Infinite loop for auto restart if app closed or crashed
while :
  do
    python $EXPATH/midi.py
  done
