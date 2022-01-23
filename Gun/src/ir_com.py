import machine

from ir_rx.nec import NEC_16
from ir_rx.print_error import print_error
from ir_tx.nec import NEC


class Communicator:
    def __init__(self, receivePin: int = 32, transmitPin: int = 12):
        self.receiver = NEC_16(machine.Pin(receiverPin, machine.Pin.IN), self.receive)
        self.receiver.error_function(print_error)

        self.transmitter = NEC(machine.Pin(transmitPin, machine.Pin.OUT))

    def receive(self, data, addr, ctrl):
        print("Callback is called")
        if data < 0:  # NEC protocol sends repeat codes.
            print("Repeat code.")
        else:
            print("Data {:02x} Addr {:04x}".format(data, addr))

    def transmit(self, address, data):
        print("Sending: " + str(data) + ", to: " + str(address))
        self.transmitter.transmit(address, data)
