import gc
import time

import machine
import uasyncio as asyncio

from gun import Gun
from ir_com import Communicator
from primitives.pushbutton import Pushbutton


async def callback():
    print("Callback called: ")


async def main():
    print("Started main function")
    gun = Gun()

    btnpin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
    btn = Pushbutton(btnpin)

    btn.press_func(callback)  # Callback expects tuple

    while True:
        await asyncio.sleep(1)


print("Starting")
asyncio.run(main())

# buttonpin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
