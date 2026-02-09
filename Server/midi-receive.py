#!/usr/bin/python3

import tkinter as tk
import subprocess


def getServerAddress():
    server = subprocess.check_output("/usr/bin/head -n 1 /tmp/log.log", shell=True)
    return server.decode("utf-8")

def taillog():
    s = subprocess.check_output("/usr/bin/tail -n 10 /tmp/log.log", shell=True)
    return s.decode("utf-8")

def refreshlog():
    tb2.config(state='normal')
    tb2.delete("1.0", "end")
    tb2.insert(tk.END, taillog())
    tb2.config(state='disabled')
    root.after(1000, refreshlog)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player-Server")
    root.geometry("800x480") #for 5 inch touch display
    root.tk.call('tk', 'scaling', 2) #default 1.25; 3 too large
    #maximized
    #root.attributes('-zoomed', True)
    #fullscreen
    root.attributes('-fullscreen', True)

    tb1 = tk.Text(
        root,
        height = 1,
        width = 30,
        state='normal'
        )

    tb1.place(x=400, y=50, anchor=tk.CENTER)

    tb1.insert(tk.END, getServerAddress())

    tb2 = tk.Text(
        root,
        height = 10,
        width = 80,
        state='disabled'
        )

    tb2.place(x=400, y=200, anchor=tk.CENTER)


    print(taillog())
    refreshlog()

    root.mainloop()
