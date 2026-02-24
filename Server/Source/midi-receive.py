#!/usr/bin/python

import mido
from mido import sockets
import subprocess

def getClientIPlan():
    cIP = subprocess.check_output("/usr/sbin/nmcli -f IP4.ADDRESS device show $(nmcli device status | grep ethernet | awk '{print $1}') | /usr/sbin/awk '{print $2}' | cut -d '/' -f 1", shell=True).strip()
    return cIP.decode("utf-8")

#Automatically set with MIDO_DEFAULT_OUTPUT environment variable exported via start script
port = mido.open_output()



address = getClientIPlan() + ':9080'

print(f'Serving on {address}')
print('Port: ' + port.name)

host, webport = sockets.parse_address(address)

with sockets.PortServer(host, webport) as server:
    while True:
        try:
            client = server.accept(block=False)
            if client:
                for message in client:
                    print(message)
                    port.send(message)
        except KeyboardInterrupt:
            break
