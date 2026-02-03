#!/bin/bash

#Path to midi.py
EXPATH=/home/user/Documents/MIDI-Player-GUI

#Get MIDI device, if none is available, fallback to "Through"
if $(python $EXPATH/Source/mido-getDevice.py | grep "CH345" > /dev/null)
then
  echo "Device CH345 found!"
  DEVICE=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(CH345[^']*\)'.*/\1/p")
  sed -i "s|^port = mido\.open_output.*|port = mido.open_output(\"$DEVICE\")|" $EXPATH/Source/midi.py
else
  echo "Device CH345 not found, falling back to Through!"
  DEVICE=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(Midi Through[^']*\)'.*/\1/p")
  sed -i "s|^port = mido\.open_output.*|port = mido.open_output(\"$DEVICE\")|" $EXPATH/Source/midi.py
fi

#Default path for USB-Mount on Raspberry Pi OS
cd /media/user

#Give current IP if connected to Wifi
ifconfig | grep inet

#Infinite loop for auto restart if app closed or crashed
while :
  do
    python $EXPATH/Source/midi.py
  done
