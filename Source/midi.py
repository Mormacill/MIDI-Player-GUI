#!/usr/bin/python3

import tkinter as tk
from tkinter.filedialog import askopenfilename

from threading import Thread

import mido
import re
import time

VER = '1.2-EL'

#TODO
# * DONE -> if ownPanic() is called (e.g. stop pressed), leave register untouched
# * Resize interface for 10,1' touch screen
# * Set up with Fedora IOT
# * Create a server-client network for communication between organ console and organ control unit and include "connection established" infos on interface
# * Shutdown and reboot buttons on maintenance interface
# * USB default mount point
# * Splash screen

#Qsynth
#port = mido.open_output('Midi Through:Midi Through Port-0 14:0')

#CH345 USB-Midi
#port = mido.open_output('CH345:CH345 MIDI 1 28:0')

#Automatically set with bash start script
port = mido.open_output('Midi Through:Midi Through Port-0 14:0')

###
hwRegChan = 2     #Stops all run via the pedal-interface since there are unused ports
hiwRegChan = 2
pedRegChan = 2

hw_1RegKey = 68   #Counting upwards from the third bus of the interface since the pedal-interface only uses two buses. 68 corresponds to contact 33
hw_2RegKey = 69
hw_3RegKey = 70
hw_4RegKey = 71

hiw_1RegKey = 72
hiw_2RegKey = 73
hiw_3RegKey = 74
hiw_4RegKey = 75

ped_1RegKey = 76
ped_2RegKey = 77
###

#somehow port.panic() doesnt work on CH345
def ownPanic():
    for ch in range(1):                   #This organ only has 3 divisions, so cleaning the first 3 channel is enough; Here only clearing Manuals since Pedal has Stops included which shall not be cleared
      for noteNumber in range(36, 97):    #36 to 96 is enough since 0 to 35 and 97 to 127 are not used
        msg = mido.Message('note_off', channel=ch, note=noteNumber)
        port.send(msg)

    for noteNumber in range(36, 63):      #Clearing for Pedal Keys (36 to 63), only channel 2; 68 to 77 are all stops located
      msg = mido.Message('note_off', channel=2, note=noteNumber)
      port.send(msg)

def ownPanic_spec(ch):
    for noteNumber in range(36, 97):      #36 to 96 is enough since 0 to 35 and 97 to 127 are not used
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
    writeHW1(hwRegChan, hw_1RegKey)
    hw_2.set(v)
    writeHW2(hwRegChan, hw_2RegKey)
    hw_3.set(v)
    writeHW3(hwRegChan, hw_3RegKey)
    hw_4.set(v)
    writeHW4(hwRegChan, hw_4RegKey)

    hiw_1.set(v)
    writeHiW1(hiwRegChan, hiw_1RegKey)
    hiw_2.set(v)
    writeHiW2(hiwRegChan, hiw_2RegKey)
    hiw_3.set(v)
    writeHiW3(hiwRegChan, hiw_3RegKey)
    hiw_4.set(v)
    writeHiW4(hiwRegChan, hiw_4RegKey)

    ped_1.set(v)
    writePed1(pedRegChan, ped_1RegKey)
    ped_2.set(v)
    writePed2(pedRegChan, ped_2RegKey)

    kop_1.set(v)
    kop1_switchOff()
    kop_2.set(v)
    kop2_switchOff()
    kop_3.set(v)
    kop3_switchOff()


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

#Wartungsfenster
def maintenance_window():
    mwindow = tk.Toplevel(root)
    mwindow.configure(bg='light goldenrod yellow')
    mwindow.geometry("1280x800") #for 10.1 inch touch display
    mwindow.attributes('-fullscreen', True)

    tune_werk = tk.IntVar(mwindow, value=0)

    array_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "h", "c'", "c#'", "d'", "d#'", "e'", "f'", "f#'", "g'", "g#'", "a'", "a#'", "h'", "c''", "c#''", "d''", "d#''", "e''", "f''", "f#''", "g''", "g#''", "a''", "a#''", "h''", "c'''", "c#'''", "d'''", "d#'''", "e'''", "f'''", "f#'''", "g'''", "g#'''", "a'''", "a#'''", "h'''", "c''''"]

    key = tk.IntVar(mwindow, value=36)

    mwindow_close = tk.Button(
      mwindow,
      text="Schließen",
      command=lambda: [mwindow.destroy(), ownPanic()]
      )
    mwindow_close.place(x=280, y=440, anchor=tk.CENTER)

    mwindow_tune_hw = tk.Button(
      mwindow,
      text="Hauptwerk",
      bg='red',
      command=lambda: [ownPanic(), tune_werk.set(0), mwindow_tune_hw.config(bg='red'), mwindow_tune_hiw.config(bg='light gray'), mwindow_tune_ped.config(bg='light gray')]
      )

    mwindow_tune_hw.place(x=100, y=50, anchor=tk.CENTER)

    mwindow_tune_hiw = tk.Button(
      mwindow,
      text="Hinterwerk",
      command=lambda: [ownPanic(), tune_werk.set(1), mwindow_tune_hw.config(bg='light gray'), mwindow_tune_hiw.config(bg='red'), mwindow_tune_ped.config(bg='light gray')]
      )

    mwindow_tune_hiw.place(x=280, y=50, anchor=tk.CENTER)

    mwindow_tune_ped = tk.Button(
      mwindow,
      text="Pedal",
      command=lambda: [ownPanic(), tune_werk.set(2), mwindow_tune_hw.config(bg='light gray'), mwindow_tune_hiw.config(bg='light gray'), mwindow_tune_ped.config(bg='red')]
      )

    mwindow_tune_ped.place(x=460, y=50, anchor=tk.CENTER)

    mwindow_tune_START = tk.Button(
      mwindow,
      text="Start",
      command=lambda: [key.set(36), noteON(tune_werk.get(), key.get()), current_tone_box.config(state='normal'), current_tone_box.delete("1.0", "end"), current_tone_box.tag_configure("center", justify='center'), current_tone_box.insert(tk.END, array_notes[key.get()-36]), current_tone_box.tag_add("center", "1.0", "end"), current_tone_box.config(state='disabled')]
      )

    mwindow_tune_START.place(x=280, y=120, anchor=tk.CENTER)

    mwindow_next_tone = tk.Button(
      mwindow,
      text=">",
      command=lambda: [noteOFF(tune_werk.get(), key.get()), key.set(key.get()+1), noteON(tune_werk.get(), key.get()), current_tone_box.config(state='normal'), current_tone_box.delete("1.0", "end"), current_tone_box.tag_configure("center", justify='center'), current_tone_box.insert(tk.END, array_notes[key.get()-36]), current_tone_box.tag_add("center", "1.0", "end"), current_tone_box.config(state='disabled'), print(tune_werk.get(), key.get())]
      )

    mwindow_next_tone.place(x=460, y=220, anchor=tk.CENTER)

    mwindow_previous_tone = tk.Button(
      mwindow,
      text="<",
      command=lambda: [noteOFF(tune_werk.get(), key.get()), key.set(key.get()-1), noteON(tune_werk.get(), key.get()), current_tone_box.config(state='normal'), current_tone_box.delete("1.0", "end"), current_tone_box.tag_configure("center", justify='center'), current_tone_box.insert(tk.END, array_notes[key.get()-36]), current_tone_box.tag_add("center", "1.0", "end"), current_tone_box.config(state='disabled'), print(tune_werk.get(), key.get())]
      )

    mwindow_previous_tone.place(x=100, y=220, anchor=tk.CENTER)

    current_tone_Label = tk.Label(
        mwindow,
        text='Aktueller Ton',
        bg='light goldenrod yellow'
        )

    current_tone_Label.place(x=280, y=190, anchor=tk.CENTER)

    current_tone_box = tk.Text(
        mwindow,
        height = 1,
        width = 10,
        state='disabled',
        font=("", 14)
        )

    current_tone_box.place(x=280, y=220, anchor=tk.CENTER)

    mwindow_tune_STOP = tk.Button(
      mwindow,
      text="Stop",
      command=ownPanic
      )

    mwindow_tune_STOP.place(x=280, y=300, anchor=tk.CENTER)

    device = tk.Text(
        mwindow,
        height = 1,
        width = 60,
        state='disabled'
        )

    device.place(x=280, y=370, anchor=tk.CENTER)

    device.config(state='normal')
    device.delete("1.0", "end")
    device.tag_configure("center", justify='center')
    device.insert(tk.END, port)
    device.tag_add("center", "1.0", "end")
    device.config(state='disabled')

##########################################################

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player")
    root.geometry("1280x800") #for 10.1 inch touch display
    root.tk.call('tk', 'scaling', 3) #default 1.25; 3 too large
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
        #font=("", 14),
        command=lambda: Thread(target = playmidi).start()
        )

    start.place(x=280, y=50, anchor=tk.CENTER)

    tb = tk.Text(
        root,
        height = 1,
        width = 30,
        state='disabled'
        )

    tb.place(x=280, y=120, anchor=tk.CENTER)

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

    speedSlider.place(x=280, y=280, anchor=tk.CENTER)

    speedReset = tk.Button(
        root,
        text='reset',
        command=lambda: speed_multiplier.set(100)
        )

    speedReset.place(x=280, y=380, anchor=tk.CENTER)

    registerReset = tk.Button(
        root,
        text='0',
        font=("", 7),
        command=lambda: regres(0)
        )

    registerReset.place(x=750, y=400, anchor=tk.CENTER)

    registerTutti = tk.Button(
        root,
        text='T',
        font=("", 7),
        command=lambda: regres(1)
        )

    registerTutti.place(x=660, y=400, anchor=tk.CENTER)

    stop = tk.Button(
        root,
        text='stop',
        command=stopplayback
        )

    stop.place(x=280, y=185, anchor=tk.CENTER)

    quit = tk.Button(
        root,
        text='quit',
        command=quit
        )

    quit.place(x=80, y=440, anchor=tk.CENTER)

    HW_Label = tk.Label(
        root,
        text='Hauptwerk',
        font=("", 7),
        )

    HW_Label.place(x=486, y=190, anchor=tk.NW)

    HIW_Label = tk.Label(
        root,
        text='Hinterwerk',
        font=("", 7)
        )

    HIW_Label.place(x=650, y=190, anchor=tk.NW)

    PED_Label = tk.Label(
        root,
        text='Pedal',
        font=("", 7)
        )

    PED_Label.place(x=486, y=370, anchor=tk.NW)

    KOP_Label = tk.Label(
        root,
        text='Koppeln',
        font=("", 7)
        )

    KOP_Label.place(x=650, y=40, anchor=tk.NW)

    hw_rohr = tk.Checkbutton(
        root,
        text='Rohrflöte 8\'',
        font=("", 7),
        variable=hw_1,
        command=lambda: writeHW1(hwRegChan,hw_1RegKey)
        )

    hw_rohr.place(x=450, y=230, anchor=tk.NW)

    hw_prinz = tk.Checkbutton(
        root,
        text='Prinzipal 4\'',
        font=("", 7),
        variable=hw_2,
        #font=("", 10),
        command=lambda: writeHW2(hwRegChan,hw_2RegKey)
        )

    hw_prinz.place(x=450, y=260, anchor=tk.NW)

    hw_okt = tk.Checkbutton(
        root,
        text='Oktave 2\'',
        font=("", 7),
        variable=hw_3,
        command=lambda: writeHW3(hwRegChan,hw_3RegKey)
        )

    hw_okt.place(x=450, y=290, anchor=tk.NW)

    hw_mix = tk.Checkbutton(
        root,
        text='Mixtur',
        font=("", 7),
        variable=hw_4,
        command=lambda: writeHW4(hwRegChan,hw_4RegKey)
        )

    hw_mix.place(x=450, y=320, anchor=tk.NW)

    hiw_ged = tk.Checkbutton(
        root,
        text='Gedackt 8\'',
        font=("", 7),
        variable=hiw_1,
        command=lambda: writeHiW1(hiwRegChan,hiw_1RegKey)
        )

    hiw_ged.place(x=614, y=230, anchor=tk.NW)

    hiw_gedfl = tk.Checkbutton(
        root,
        text='Ged. Flöte 4\'',
        font=("", 7),
        variable=hiw_2,
        command=lambda: writeHiW2(hiwRegChan,hiw_2RegKey)
        )

    hiw_gedfl.place(x=614, y=260, anchor=tk.NW)

    hiw_wald = tk.Checkbutton(
        root,
        text='Waldflöte 2\'',
        font=("", 7),
        variable=hiw_3,
        command=lambda: writeHiW3(hiwRegChan,hiw_3RegKey)
        )

    hiw_wald.place(x=614, y=290, anchor=tk.NW)

    hiw_siff = tk.Checkbutton(
        root,
        text='Sifflöte',
        font=("", 7),
        variable=hiw_4,
        command=lambda: writeHiW4(hiwRegChan,hiw_4RegKey)
        )

    hiw_siff.place(x=614, y=320, anchor=tk.NW)

    ped_sub = tk.Checkbutton(
        root,
        text='Subbaß 16\'',
        font=("", 7),
        variable=ped_1,
        command=lambda: writePed1(pedRegChan,ped_1RegKey)
        )

    ped_sub.place(x=450, y=410, anchor=tk.NW)

    ped_nacht = tk.Checkbutton(
        root,
        text='Nachthorn 4\'',
        font=("", 7),
        variable=ped_2,
        command=lambda: writePed2(pedRegChan,ped_2RegKey)
        )

    ped_nacht.place(x=450, y=440, anchor=tk.NW)

    kop_man = tk.Checkbutton(
        root,
        text='II/I',
        font=("", 7),
        variable=kop_1,
        command=kop1_switchOff
        )

    kop_man.place(x=614, y=80, anchor=tk.NW)

    kop_pedI = tk.Checkbutton(
        root,
        text='I/Ped',
        font=("", 7),
        variable=kop_2,
        command=kop2_switchOff
        )

    kop_pedI.place(x=614, y=110, anchor=tk.NW)

    kop_pedII = tk.Checkbutton(
        root,
        text='II/Ped',
        font=("", 7),
        variable=kop_3,
        command=kop3_switchOff
        )

    kop_pedII.place(x=614, y=140, anchor=tk.NW)

    maintenance = tk.Button(
      root,
      text="Wartung",
      command=maintenance_window
      )

    maintenance.place(x=280, y=440, anchor=tk.CENTER)

    Version_Label = tk.Label(
      root,
      text='Version ' + tk.StringVar(value=VER).get(),
      font=("", 7)
      )

    Version_Label.place(x=660, y=440, anchor=tk.NW)

    root.mainloop()
