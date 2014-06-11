#!/usr/bin/python
import socket
import string
import time

recieve_address = ('10.0.0.50', 12010)
send_address = ('127.0.0.1', 12011)

mappings = {
    '*': 1000000000,
    '/game/reset':     0,
    '/game/setNames':    0,
    '/game/gameWin':          0,
    '/scene/youaredead':    0,
}

listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen.bind(recieve_address)
listen.settimeout(0.05)

messages = {}
times = []

while True:
    data = None
    try:
        data, addr = listen.recvfrom(4096)
    except socket.timeout:
        pass

    now = time.time()

    if data:
        address_terminator = string.find(data, "\0")
        osc_address = data[0:address_terminator]

        timeout = mappings.get(osc_address, mappings['*'])
        messages[now + timeout] = data
        times = messages.keys()
        times.sort()

    while True:
        if times and now >= times[0]:
            timestamp = times.pop(0)
            listen.sendto(messages[timestamp], send_address)
            del messages[timestamp]
        else:
            break
