# main.py

import time

import machine

from ir_rx.nec import NEC_8
from ir_tx.nec import NEC


def callback(data, addr, ctrl):
    print("Callback is called")
    if data < 0:  # NEC protocol sends repeat codes.
        print("Repeat code.")
    else:
        print("Data {:02x} Addr {:04x}".format(data, addr))


receiver = NEC_8(machine.Pin(32, machine.Pin.IN), callback)

transmitter = NEC(machine.Pin(12, machine.Pin.OUT))


button = 0
buttonPin = machine.Pin(26, machine.Pin.IN)

i = 0
while 1:
    if buttonPin.value() and not button:
        button = 1
        print("Button went low")

    elif not buttonPin.value() and button:
        button = 0
        print("Button went high" + str(i))
        i += 1
        transmitter.transmit(1, i)
