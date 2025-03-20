import tkinter as tk
from tkinter.filedialog import askopenfilename

import mido
import time

port = mido.open_output('FLUID Synth (2):Synth input port (2:0) 128:0')

def quit():
    root.destroy()
    port.panic()


def stopplayback():
    global running
    running = False

def playmidi():
    global running
    running = True
    filename = askopenfilename(filetypes = [('Midi Files', '*.mid')])
    mid = mido.MidiFile(filename)
    estplaytime = mid.length / 60
    tb.config(state='normal')
    tb.delete("1.0", "end")
    tb.tag_configure("center", justify='center')
    tb.insert(tk.END, "Spieldauer: " + "%.2f" % estplaytime + " Minuten")
    tb.tag_add("center", "1.0", "end")
    tb.config(state='disabled')
    for msg2 in mid.play():
        port.send(msg2)
        root.update()
        if running == False:
            port.panic()
            break

def readRegister():
    print(hw_1.get(), hw_2.get(), hw_3.get(), hw_4.get())
    print(hiw_1.get(), hiw_2.get(), hiw_3.get(), hiw_4.get())
    print(ped_1.get(), ped_2.get())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player")
    root.geometry("500x330")
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

    start = tk.Button(
        root,
        text='Midi-Datei auswählen...',
        command=playmidi
        )

    tb = tk.Text(
        root,
        height = 2,
        width = 30,
        state='disabled'
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
    stop.place(x=110, y=100)
    quit.place(x=110, y=210)

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

    hw_rohr = tk.Checkbutton(
        root,
        text='Rohrflöte 8\'',
        variable=hw_1,
        command=readRegister
        )

    hw_prinz = tk.Checkbutton(
        root,
        text='Prinzipal 4\'',
        variable=hw_2,
        #font=("", 10),
        command=readRegister
        )

    hw_okt = tk.Checkbutton(
        root,
        text='Oktave 2\'',
        variable=hw_3,
        command=readRegister
        )

    hw_mix = tk.Checkbutton(
        root,
        text='Mixtur',
        variable=hw_4,
        command=readRegister
        )

    hiw_ged = tk.Checkbutton(
        root,
        text='Gedackt 8\'',
        variable=hiw_1,
        command=readRegister
        )

    hiw_gedfl = tk.Checkbutton(
        root,
        text='Ged. Flöte 4\'',
        variable=hiw_2,
        command=readRegister
        )

    hiw_wald = tk.Checkbutton(
        root,
        text='Waldflöte 2\'',
        variable=hiw_3,
        command=readRegister
        )

    hiw_siff = tk.Checkbutton(
        root,
        text='Sifflöte',
        variable=hiw_4,
        command=readRegister
        )

    ped_sub = tk.Checkbutton(
        root,
        text='Subbaß 16\'',
        variable=ped_1,
        command=readRegister
        )

    ped_nacht = tk.Checkbutton(
        root,
        text='Nachhorn 4\'',
        variable=ped_2,
        command=readRegister
        )

    HW_Label.place(x=350, y=10)
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

    msg = mido.Message('note_on', channel=0, note=60)
    msg3 = mido.Message('note_off', channel=0, note=60)

root.mainloop()
