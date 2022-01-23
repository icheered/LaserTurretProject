import machine

from ir_rx.nec import NEC_16
from ir_rx.print_error import print_error
from ir_tx.nec import NEC

import uasyncio as asyncio


class Communicator:
    def __init__(self, transmitPin: int = 12, receivePin: int = 14):
        self._receiver = NEC_16(machine.Pin(receivePin, machine.Pin.IN), self.receive)
        self._receiver.error_function(print_error)

        self._transmitter = NEC(machine.Pin(transmitPin, machine.Pin.OUT))

        # Pre-define message callback function
        self._messageCallback = None

    def setMessagehandlerCallback(self, messageHandler):
        self._messageCallback = messageHandler

    def receive(self, data, addr, ctrl):
        print("IR Message is received")
        if data < 0:  # NEC protocol sends repeat codes.
            print("Repeat code.")
        elif self._messageCallback is None:
            print("messagehandler callback wasn't initialized")
        else:
            print("Data {:02x} Addr {:04x}".format(data, addr))
            self._messageCallback(data, addr)

    async def transmit(self, address, data):
        # print("Sending: " + str(data) + ", to: " + str(address))
        self._transmitter.transmit(address, data)
