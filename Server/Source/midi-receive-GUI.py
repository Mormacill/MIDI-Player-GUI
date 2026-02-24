#!/usr/bin/python3

import tkinter as tk
import subprocess


def getServerAddress():
    server = subprocess.check_output("/usr/bin/head -n 1 /tmp/log.log", shell=True)
    return server.decode("utf-8")

def taillog():
    s = subprocess.check_output("/usr/bin/tail -n 15 /tmp/log.log", shell=True)
    return s.decode("utf-8")

def refreshlog():
    tb2.config(state='normal')
    tb2.delete("1.0", "end")
    tb2.insert(tk.END, taillog())
    tb2.config(state='disabled')
    root.after(100, refreshlog)

#get client IP Adress on wifi
def getClientIPwifi():
    cIP = subprocess.check_output("/usr/sbin/nmcli -f IP4.ADDRESS device show $(nmcli device status | grep wifi | awk '{print $1}') | /usr/sbin/awk '{print $2}'", shell=True)
    return cIP.decode("utf-8")

#get client IP Adress on LAN
def getClientIPlan():
    cIP = subprocess.check_output("/usr/sbin/nmcli -f IP4.ADDRESS device show $(nmcli device status | grep ethernet | awk '{print $1}') | /usr/sbin/awk '{print $2}'", shell=True)
    return cIP.decode("utf-8")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MIDI-Player-Server")
    root.geometry("800x480") #for 5 inch touch display
    root.tk.call('tk', 'scaling', 1)
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
        height = 15,
        width = 80,
        state='disabled'
        )

    tb2.place(x=400, y=200, anchor=tk.CENTER)

    clientIP_LAN = tk.Text(
        root,
        height = 1,
        width = 18,
        state='disabled'
        )

    clientIP_LAN.place(x=400, y=360, anchor=tk.CENTER)

    clientIP_LAN.config(state='normal')
    clientIP_LAN.delete("1.0", "end")
    clientIP_LAN.tag_configure("center", justify='center')
    clientIP_LAN.insert(tk.END, getClientIPlan())
    clientIP_LAN.tag_add("center", "1.0", "end")
    clientIP_LAN.config(state='disabled')

    clientIP_LAN_Label = tk.Label(
        root,
        text='LAN-IP:',
        #bg='light goldenrod yellow'
        )

    clientIP_LAN_Label.place(x=400, y=340, anchor=tk.CENTER)

    clientIP_wifi = tk.Text(
        root,
        height = 1,
        width = 18,
        state='disabled'
        )

    clientIP_wifi.place(x=400, y=400, anchor=tk.CENTER)

    clientIP_wifi.config(state='normal')
    clientIP_wifi.delete("1.0", "end")
    clientIP_wifi.tag_configure("center", justify='center')
    clientIP_wifi.insert(tk.END, getClientIPwifi())
    clientIP_wifi.tag_add("center", "1.0", "end")
    clientIP_wifi.config(state='disabled')

    clientIP_wifi_Label = tk.Label(
        root,
        text='WLAN-IP:',
        #bg='light goldenrod yellow'
        )

    clientIP_wifi_Label.place(x=400, y=380, anchor=tk.CENTER)

#    device = tk.Text(
#        root,
#        height = 1,
#        width = 40,
#        state='disabled'
#        )
#
#    device.place(x=400, y=440, anchor=tk.CENTER)
#
#    device.config(state='normal')
#    device.delete("1.0", "end")
#    device.tag_configure("center", justify='center')
#    device.insert(tk.END, port.name)
#    device.tag_add("center", "1.0", "end")
#    device.config(state='disabled')
#
#    device_Label = tk.Label(
#        root,
#        text='Gerät:',
#        #bg='light goldenrod yellow'
#        )
#
#    device_Label.place(x=400, y=420, anchor=tk.CENTER)

    print(taillog())
    refreshlog()

    root.mainloop()
