import tkinter as tk
from tkinter.filedialog import askopenfilename

from threading import Thread

import mido
import re
import time

#Qsynth
port = mido.open_output('Midi Through:Midi Through Port-0 14:0')

#CH345 USB-Midi
#port = mido.open_output('CH345:CH345 MIDI 1 28:0')

#somehow port.panic() doesnt work on CH345
def ownPanic():
    for ch in range(15):
      for noteNumber in range(127):
        msg = mido.Message('note_off', channel=ch, note=noteNumber)
        port.send(msg)

def ownPanic_spec(ch):
    for noteNumber in range(127):
        msg = mido.Message('note_off', channel=ch, note=noteNumber)
        port.send(msg)

def quit():
    stopplayback()
    ownPanic()
    root.destroy()

def stopplayback():
    global running
    running = False

def playmidi():
    global running
    running = False
    filename = askopenfilename(filetypes = [('Midi Files', '*.mid')])
    mid = mido.MidiFile(filename)
    estplaytime = mid.length / 60
    tb.config(state='normal')
    tb.delete("1.0", "end")
    tb.tag_configure("center", justify='center')
    tb.insert(tk.END, "Spieldauer: " + "%.2f" % (estplaytime/(speed_multiplier.get()/100)) + " Minuten")
    tb.tag_add("center", "1.0", "end")
    tb.config(state='disabled')
    running = True

    for msg in mid:
      time.sleep(msg.time * 1/((speed_multiplier.get())/100))
      if not msg.is_meta:
        if kop_1.get(): #II/I
          msg_re = re.sub("channel=0", "channel=1", str(msg))
          port.send(mido.Message.from_str(msg_re))
        if kop_2.get(): #I/Ped
          msg2_re = re.sub("channel=2", "channel=0", str(msg))
          port.send(mido.Message.from_str(msg2_re))
        if kop_3.get(): #II/Ped
          msg3_re = re.sub("channel=2", "channel=1", str(msg))
          port.send(mido.Message.from_str(msg3_re))
        port.send(msg)

    #for msg2 in mid.play():
        #msg2_string = str(msg2)
        #msg2_re = re.sub("channel=0", "channel=1", msg2_string)
        #mido.Message.from_str(msg2_re)
        #port.send(mido.Message.from_str(msg2_re))

        #root.update()
        if running == False:            
          ownPanic()
          break

def readRegister():
    print(hw_1.get(), hw_2.get(), hw_3.get(), hw_4.get())
    print(hiw_1.get(), hiw_2.get(), hiw_3.get(), hiw_4.get())
    print(ped_1.get(), ped_2.get())

def noteON(chan, key):
    msg = mido.Message('note_on', channel=chan, note=key)
    port.send(msg)

def noteOFF(chan, key):
    msg = mido.Message('note_off', channel=chan, note=key)
    port.send(msg)

def writeHW1(chan, key):
    if hw_1.get() == 1:
      print(key)
      noteON(chan, key)
    elif hw_1.get() == 0:
      noteOFF(chan, key)

def writeHW2(chan, key):
    if hw_2.get() == 1:
      print(key)
      noteON(chan, key)
    elif hw_2.get() == 0:
      noteOFF(chan, key)

def writeHW3(chan, key):
    if hw_3.get() == 1:
      print(key)
      noteON(chan, key)
    elif hw_3.get() == 0:
      noteOFF(chan, key)

def writeHW4(chan, key):
    if hw_4.get() == 1:
      print(key)
      noteON(chan, key)
    if hw_4.get() == 0:
      noteOFF(chan, key)

##########################################################

def writeHiW1(chan, key):
    if hiw_1.get() == 1:
      print(key)
      noteON(chan, key)
    elif hiw_1.get() == 0:
      noteOFF(chan, key)

def writeHiW2(chan, key):
    if hiw_2.get() == 1:
      print(key)
      noteON(chan, key)
    elif hiw_2.get() == 0:
      noteOFF(chan, key)

def writeHiW3(chan, key):
    if hiw_3.get() == 1:
      print(key)
      noteON(chan, key)
    elif hiw_3.get() == 0:
      noteOFF(chan, key)

def writeHiW4(chan, key):
    if hiw_4.get() == 1:
      print(key)
      noteON(chan, key)
    if hiw_4.get() == 0:
      noteOFF(chan, key)

##########################################################

def writePed1(chan, key):
    if ped_1.get() == 1:
      print(key)
      noteON(chan, key)
    if ped_1.get() == 0:
      noteOFF(chan, key)

def writePed2(chan, key):
    if ped_2.get() == 1:
      print(key)
      noteON(chan, key)
    if ped_2.get() == 0:
      noteOFF(chan, key)

##########################################################

def kop1_switchOff():
    if not kop_1.get():
      ownPanic_spec(1) #Channel 1 Mido, Channel 2 Mdidi

def kop2_switchOff():
    if not kop_2.get():
      ownPanic_spec(0) #Channel 0 Mido, Channel 1 Mdidi

def kop3_switchOff():
    if not kop_3.get():
      ownPanic_spec(1) #Channel 1 Mido, Channel 2 Mdidi

##########################################################

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player")
    root.geometry("600x330")
    root.tk.call('tk', 'scaling',1.25)
    #root.attributes('-zoomed', True)

    hw_1 = tk.IntVar()
    hw_2 = tk.IntVar()
    hw_3 = tk.IntVar()
    hw_4 = tk.IntVar()

    hiw_1 = tk.IntVar()
    hiw_2 = tk.IntVar()
    hiw_3 = tk.IntVar()
    hiw_4 = tk.IntVar()

    ped_1 = tk.IntVar()
    ped_2 = tk.IntVar()

    kop_1 = tk.IntVar()
    kop_2 = tk.IntVar()
    kop_3 = tk.IntVar()

    speed_multiplier = tk.IntVar()
    speed_multiplier.set(100)

    start = tk.Button(
        root,
        text='Midi-Datei auswählen...',
        command=lambda: Thread(target = playmidi).start()
        )

    tb = tk.Text(
        root,
        height = 2,
        width = 30,
        state='disabled'
        )

    speedSlider = tk.Scale(
        root,
        from_=70,
        to=130,
        orient=tk.HORIZONTAL,
        relief=tk.FLAT,
        length=200,
        tickinterval=30,
        variable=speed_multiplier
        )

    speedReset = tk.Button(
        root,
        text='Reset',
        command=lambda: speed_multiplier.set(100)
        )

    stop = tk.Button(
        root,
        text='stop',
        command=stopplayback
        )

    quit = tk.Button(
        root,
        text='Quit',
        command=quit
        )

    start.place(x=50, y=10)
    tb.place(x=20, y=50)
    speedSlider.place(x=36, y=140)
    speedReset.place(x=105, y=200)
    stop.place(x=110, y=100)
    quit.place(x=110, y=280)

    HW_Label = tk.Label(
        root,
        text='Hauptwerk'
        )

    HIW_Label = tk.Label(
        root,
        text='Hinterwerk'
        )

    PED_Label = tk.Label(
        root,
        text='Pedal'
        )

    KOP_Label = tk.Label(
        root,
        text='Koppeln'
        )

    hw_rohr = tk.Checkbutton(
        root,
        text='Rohrflöte 8\'',
        variable=hw_1,
        command=lambda: writeHW1(0,60) #99
        )

    hw_prinz = tk.Checkbutton(
        root,
        text='Prinzipal 4\'',
        variable=hw_2,
        #font=("", 10),
        command=lambda: writeHW2(0,61) #98
        )

    hw_okt = tk.Checkbutton(
        root,
        text='Oktave 2\'',
        variable=hw_3,
        command=lambda: writeHW3(0,62) #97
        )

    hw_mix = tk.Checkbutton(
        root,
        text='Mixtur',
        variable=hw_4,
        command=lambda: writeHW4(0,63) #96
        )

    hiw_ged = tk.Checkbutton(
        root,
        text='Gedackt 8\'',
        variable=hiw_1,
        command=lambda: writeHiW1(1,60) #99
        )

    hiw_gedfl = tk.Checkbutton(
        root,
        text='Ged. Flöte 4\'',
        variable=hiw_2,
        command=lambda: writeHiW2(1,61) #98
        )

    hiw_wald = tk.Checkbutton(
        root,
        text='Waldflöte 2\'',
        variable=hiw_3,
        command=lambda: writeHiW3(1,62) #97
        )

    hiw_siff = tk.Checkbutton(
        root,
        text='Sifflöte',
        variable=hiw_4,
        command=lambda: writeHiW4(1,63) #96
        )

    ped_sub = tk.Checkbutton(
        root,
        text='Subbaß 16\'',
        variable=ped_1,
        command=lambda: writePed1(2,60)
        )

    ped_nacht = tk.Checkbutton(
        root,
        text='Nachthorn 4\'',
        variable=ped_2,
        command=lambda: writePed2(2,61)
        )

    kop_man = tk.Checkbutton(
        root,
        text='II/I',
        variable=kop_1,
        command=kop1_switchOff
        )

    kop_pedI = tk.Checkbutton(
        root,
        text='I/Ped',
        variable=kop_2,
        command=kop2_switchOff
        )

    kop_pedII = tk.Checkbutton(
        root,
        text='II/Ped',
        variable=kop_3,
        command=kop3_switchOff
        )

    HW_Label.place(x=350, y=20)
    hw_rohr.place(x=350, y=40)
    hw_prinz.place(x=350, y=60)
    hw_okt.place(x=350, y=80)
    hw_mix.place(x=350, y=100)

    HIW_Label.place(x=350, y=140)
    hiw_ged.place(x=350, y=160)
    hiw_gedfl.place(x=350, y=180)
    hiw_wald.place(x=350, y=200)
    hiw_siff.place(x=350, y=220)

    PED_Label.place(x=350, y=260)
    ped_sub.place(x=350, y=280)
    ped_nacht.place(x=350, y=300)

    KOP_Label.place(x=500, y=20)
    kop_man.place(x=500, y=40)
    kop_pedI.place(x=500, y=60)
    kop_pedII.place(x=500, y=80)

    #msg = mido.Message('note_on', channel=0, note=60)
    #msg3 = mido.Message('note_off', channel=0, note=60)

    root.mainloop()
