#!/bin/python

import mido

#CH345 USB-Midi
port = mido.open_output('CH345:CH345 MIDI 1 28:0')

#SYSEX Messages

def midecoFactoryReset():
    msg1 = mido.Message.from_hex('F0 00 20 7A 05 01 01 01 24 F7')
    msg2 = mido.Message.from_hex('F0 00 20 7A 05 02 05 F7')
    msg3 = mido.Message.from_hex('F0 00 20 7A 05 04 00 F7')
    print(msg1.hex())
    port.send(msg1)
    print(msg2.hex())
    port.send(msg2)
    print(msg3.hex())
    port.send(msg3)
    
def midSet():
    #msg1 MIDI Channel 1 -> F0 00 20 7A 05 01 *01* 01 24 F7
    #msg1 MIDI note number 36 -> great C -> Hex 24
    #msg3 polarity reverse
    msg1 = mido.Message.from_hex('F0 00 20 7A 05 01 01 01 24 F7')
    msg2 = mido.Message.from_hex('F0 00 20 7A 05 02 05 F7')
    msg3 = mido.Message.from_hex('F0 00 20 7A 05 04 01 F7')
    print(msg1.hex())
    port.send(msg1)
    print(msg2.hex())
    port.send(msg2)
    print(msg3.hex())
    port.send(msg3)


midSet()
#midecoFactoryReset()
