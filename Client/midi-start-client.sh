#!/bin/bash

#Path to midi.py
EXPATH=/opt/MIDI-Player-GUI

#Get MIDI device, if none is available, fallback to "Through"
if $(python $EXPATH/Source/mido-getDevice.py | grep "CH345" > /dev/null)
then
  echo "Device CH345 found!"
  export MIDO_DEFAULT_OUTPUT=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(CH345[^']*\)'.*/\1/p")
else
  echo "Device CH345 not found, falling back to Through!"
  export MIDO_DEFAULT_OUTPUT=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(Midi Through[^']*\)'.*/\1/p")
fi

#Configured path for USB-Mount via udev rule
cd /media

#Give current IP if connected to Wifi
ifconfig | grep inet

#Infinite loop for auto restart if app closed or crashed
while :
  do
    python $EXPATH/Source/midi.py
  done
