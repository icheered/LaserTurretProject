# main.py

import time

import machine

from ir_rx.nec import NEC_8
from ir_tx.nec import NEC


def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print("Repeat code.")
    else:
        print("data {:02x} Addr {:04x}".format(data, addr))


rx = NEC_8(Pin(32, Pin.IN), callback)

transmitter = NEC(machine.Pin(12, machine.Pin.OUT))


print("Starting")
i = 0
while 1:
    i += 1
    transmitter.transmit(1, i)
    time.sleep(1)
