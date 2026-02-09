#!/bin/bash

#Path to midi-receive.py
EXPATH=/opt/MIDI-Player-GUI

#Get MIDI device, if none is available, fallback to "Through"
if $(python $EXPATH/Source/mido-getDevice.py | grep "CH345" > /dev/null)
then
  echo "Device CH345 found!"
  DEVICE=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(CH345[^']*\)'.*/\1/p")
  sed -i "s|^port = mido\.open_output.*|port = mido.open_output(\"$DEVICE\")|" $EXPATH/Source/midi-receive.py
else
  echo "Device CH345 not found, falling back to Through!"
  DEVICE=$(python $EXPATH/Source/mido-getDevice.py | sed -n "s/.*'\(Midi Through[^']*\)'.*/\1/p")
  sed -i "s|^port = mido\.open_output.*|port = mido.open_output(\"$DEVICE\")|" $EXPATH/Source/midi-receive.py
fi

#Default path for USB-Mount on Raspberry Pi OS
#cd /media/user

#Start Server
python -u $EXPATH/Source/midi-receive.py > /tmp/log.log 2>&1 &
sleep 3

#Infinite loop for auto restart if app closed or crashed
while :
  do
    python $EXPATH/Source/midi-receive-GUI.py
  done
