import uasyncio

async def blink(pin):
    while True:
        pin.on()
        await uasyncio.sleep_ms(1)
        pin.off()
        await uasyncio.sleep_ms(1)

async def main(pin):
    uasyncio.create_task(blink(pin))
    while True:
        await uasyncio.sleep(1)
    

from machine import Pin
import time
uasyncio.run(main(Pin(14, Pin.OUT)))
print("Done!")