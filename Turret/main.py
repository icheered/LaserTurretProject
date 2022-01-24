from machine import Pin
import uasyncio
from motiondetection import MotionDetector

async def blink(pin):
    while True:
        pin.on()
        await uasyncio.sleep_ms(1)
        pin.off()
        await uasyncio.sleep_ms(1)

async def main(pin):
    uasyncio.create_task(blink(pin))
    uasyncio.create_task(detect.detection())
    while True:
        await uasyncio.sleep(1)

detect = MotionDetector()
uasyncio.run(main(Pin(14, Pin.OUT)))
print("Done!")