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

def regres(v):
    hw_1.set(v)
    hw_2.set(v)
    hw_3.set(v)
    hw_4.set(v)

    hiw_1.set(v)
    hiw_2.set(v)
    hiw_3.set(v)
    hiw_4.set(v)

    ped_1.set(v)
    ped_2.set(v)

    kop_1.set(v)
    kop_2.set(v)
    kop_3.set(v)


def refreshPlaytime(estplaytime_):
    tb.config(state='normal')
    tb.delete("1.0", "end")
    tb.tag_configure("center", justify='center')
    tb.insert(tk.END, "Spieldauer: " + "%.2f" % (estplaytime_/(speed_multiplier.get()/100)) + " Minuten")
    tb.tag_add("center", "1.0", "end")
    tb.config(state='disabled')

def playmidi():
    global running
    speed_multiplier_ref = speed_multiplier.get()
    running = False
    filename = askopenfilename(filetypes = [('Midi Files', '*.mid')])
    mid = mido.MidiFile(filename)
    estplaytime = mid.length / 60
    refreshPlaytime(estplaytime)
    running = True

    for msg in mid:
      time.sleep(msg.time * 1/((speed_multiplier.get())/100))
      if not msg.is_meta:

        if speed_multiplier.get() != speed_multiplier_ref:
          refreshPlaytime(estplaytime)

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
        speed_multiplier_ref = speed_multiplier.get()

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
      ownPanic_spec(1) #Channel 1 Mido, Channel 2 Midi

def kop2_switchOff():
    if not kop_2.get():
      ownPanic_spec(0) #Channel 0 Mido, Channel 1 Midi

def kop3_switchOff():
    if not kop_3.get():
      ownPanic_spec(1) #Channel 1 Mido, Channel 2 Midi

##########################################################

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player")
    root.geometry("600x330")
    root.tk.call('tk', 'scaling', 3) #default 1.25
    #maximized
    #root.attributes('-zoomed', True)
    #fullscreen
    root.attributes('-fullscreen', True)

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
        height = 1,
        width = 30,
        state='disabled'
        )

    speedSlider = tk.Scale(
        root,
        from_=70,
        to=130,
        orient=tk.HORIZONTAL,
        relief=tk.FLAT,
        length=300,
	width=40,
        tickinterval=30,
        variable=speed_multiplier,
	font=("", 7)
        )

    speedReset = tk.Button(
        root,
        text='reset',
        command=lambda: speed_multiplier.set(100)
        )

    registerReset = tk.Button(
        root,
        text='0',
        font=("", 7),
        command=lambda: regres(0)
        )

    registerTutti = tk.Button(
        root,
        text='T',
        font=("", 7),
        command=lambda: regres(1)
        )

    stop = tk.Button(
        root,
        text='stop',
        command=stopplayback
        )

    quit = tk.Button(
        root,
        text='quit',
        command=quit
        )

    start.place(x=280, y=50, anchor=tk.CENTER)
    tb.place(x=280, y=120, anchor=tk.CENTER)
    speedSlider.place(x=280, y=280, anchor=tk.CENTER)
    speedReset.place(x=280, y=380, anchor=tk.CENTER)
    registerReset.place(x=750, y=400, anchor=tk.CENTER)
    registerTutti.place(x=660, y=400, anchor=tk.CENTER)
    stop.place(x=280, y=185, anchor=tk.CENTER)
    quit.place(x=80, y=440, anchor=tk.CENTER)

    HW_Label = tk.Label(
        root,
        text='Hauptwerk',
	font=("", 7),
        )

    HIW_Label = tk.Label(
        root,
        text='Hinterwerk',
        font=("", 7)
        )

    PED_Label = tk.Label(
        root,
        text='Pedal',
	font=("", 7)
        )

    KOP_Label = tk.Label(
        root,
        text='Koppeln',
	font=("", 7)
        )

    hw_rohr = tk.Checkbutton(
        root,
        text='Rohrflöte 8\'',
	font=("", 7),
        variable=hw_1,
        command=lambda: writeHW1(0,60) #99
        )

    hw_prinz = tk.Checkbutton(
        root,
        text='Prinzipal 4\'',
	font=("", 7),
        variable=hw_2,
        #font=("", 10),
        command=lambda: writeHW2(0,61) #98
        )

    hw_okt = tk.Checkbutton(
        root,
        text='Oktave 2\'',
	font=("", 7),
        variable=hw_3,
        command=lambda: writeHW3(0,62) #97
        )

    hw_mix = tk.Checkbutton(
        root,
        text='Mixtur',
	font=("", 7),
        variable=hw_4,
        command=lambda: writeHW4(0,63) #96
        )

    hiw_ged = tk.Checkbutton(
        root,
        text='Gedackt 8\'',
	font=("", 7),
        variable=hiw_1,
        command=lambda: writeHiW1(1,60) #99
        )

    hiw_gedfl = tk.Checkbutton(
        root,
        text='Ged. Flöte 4\'',
	font=("", 7),
        variable=hiw_2,
        command=lambda: writeHiW2(1,61) #98
        )

    hiw_wald = tk.Checkbutton(
        root,
        text='Waldflöte 2\'',
	font=("", 7),
        variable=hiw_3,
        command=lambda: writeHiW3(1,62) #97
        )

    hiw_siff = tk.Checkbutton(
        root,
        text='Sifflöte',
	font=("", 7),
        variable=hiw_4,
        command=lambda: writeHiW4(1,63) #96
        )

    ped_sub = tk.Checkbutton(
        root,
        text='Subbaß 16\'',
	font=("", 7),
        variable=ped_1,
        command=lambda: writePed1(2,60)
        )

    ped_nacht = tk.Checkbutton(
        root,
        text='Nachthorn 4\'',
	font=("", 7),
        variable=ped_2,
        command=lambda: writePed2(2,61)
        )

    kop_man = tk.Checkbutton(
        root,
        text='II/I',
	font=("", 7),
        variable=kop_1,
        command=kop1_switchOff
        )

    kop_pedI = tk.Checkbutton(
        root,
        text='I/Ped',
	font=("", 7),
        variable=kop_2,
        command=kop2_switchOff
        )

    kop_pedII = tk.Checkbutton(
        root,
        text='II/Ped',
	font=("", 7),
        variable=kop_3,
        command=kop3_switchOff
        )

    HW_Label.place(x=486, y=190, anchor=tk.NW)
    hw_rohr.place(x=450, y=230, anchor=tk.NW)
    hw_prinz.place(x=450, y=260, anchor=tk.NW)
    hw_okt.place(x=450, y=290, anchor=tk.NW)
    hw_mix.place(x=450, y=320, anchor=tk.NW)

    HIW_Label.place(x=650, y=190, anchor=tk.NW)
    hiw_ged.place(x=614, y=230, anchor=tk.NW)
    hiw_gedfl.place(x=614, y=260, anchor=tk.NW)
    hiw_wald.place(x=614, y=290, anchor=tk.NW)
    hiw_siff.place(x=614, y=320, anchor=tk.NW)

    PED_Label.place(x=486, y=370, anchor=tk.NW)
    ped_sub.place(x=450, y=410, anchor=tk.NW)
    ped_nacht.place(x=450, y=440, anchor=tk.NW)

    KOP_Label.place(x=650, y=40, anchor=tk.NW)
    kop_man.place(x=614, y=80, anchor=tk.NW)
    kop_pedI.place(x=614, y=110, anchor=tk.NW)
    kop_pedII.place(x=614, y=140, anchor=tk.NW)

    #msg = mido.Message('note_on', channel=0, note=60)
    #msg3 = mido.Message('note_off', channel=0, note=60)

    root.mainloop()
