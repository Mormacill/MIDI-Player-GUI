#!/usr/bin/python

import mido
from mido import sockets

#Automatically set with bash start script
port = mido.open_output('Midi Through:Midi Through Port-0 14:0')

address = 'localhost:9080'

print(f'Serving on {address}')

host, port = sockets.parse_address(address)

with sockets.PortServer(host, port) as server:
    while True:
        try:
            client = server.accept(block=False)
            if client:
                for message in client:
                    print(message)
                    port.send(message)
        except KeyboardInterrupt:
            break
