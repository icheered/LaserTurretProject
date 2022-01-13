import machine

from ir_tx.nec import NEC

pin = machine.Pin(12, machine.Pin.OUT)

transmitter = NEC(pin=pin)

transmitter.transmit(1, 1)


rx = machine.ADC(0)
