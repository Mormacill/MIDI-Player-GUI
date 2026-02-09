#!/bin/python

import time
import mido
from mido import Message

#CH345 USB-Midi
port = mido.open_output('CH345:CH345 MIDI 1 28:0')

#SYSEX Messages

def midTestManual():
    for x in range(64):
        key = x+36

        print("Press key to switch note", key,"on...")
        input()
        msg = Message('note_on', note=key)
        print("Switching note", key,"on\n")
        port.send(msg)

        print("Press key to switch note", key,"off...")
        input()
        msg = Message('note_off', note=key)
        print("Switching note", key,"off\n")
        port.send(msg)

def midTestAutomatic():
    for x in range(64):
        key = x+36

        msg = Message('note_on', note=key)
        print("Switching note", key,"on\n")
        port.send(msg)
        time.sleep(1)

        msg = Message('note_off', note=key)
        print("Switching note", key,"off\n")
        port.send(msg)
        time.sleep(1)

z = input("auto or manual mode?\nenter a or m\n")
if z == "a":
    midTestAutomatic()
elif z == "m":
    midTestManual()

