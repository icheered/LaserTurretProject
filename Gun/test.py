import uasyncio as asyncio
from machine import Pin

from ir_rx.nec import NEC_16


async def main():
    def callback(data, addr, ctrl):
        if data > 0:  # NEC protocol sends repeat codes.
            print("Data {:02x} Addr {:04x}".format(data, addr))

    ir = NEC_16(Pin(14, Pin.IN), callback)

    i = 0
    while True:
        i += 1
        await asyncio.sleep(5)
        print("Running: " + str(i))


import time

time.sleep(3)
print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()
