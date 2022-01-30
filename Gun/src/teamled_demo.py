import time

import machine, neopixel

neoPixel = neopixel.NeoPixel(machine.Pin(2), 8)
neoPixel.fill((255, 255, 255))
neoPixel.write()
# neoPixel[0] = (0, 255, 0)
# neoPixel.fill((255, 0, 0))


def setLed(r, g, b):
    neoPixel[0] = (r, g, b)
    neoPixel[0] = (255, 0, 0, 128)
    neoPixel.fill((r, g, b))
    neoPixel.fill((255, 0, 0))
    neoPixel.write()


while True:
    print("Printing colors")
    setLed(255, 0, 0)
    time.sleep(1)
    setLed(0, 255, 0)
    time.sleep(1)
    setLed(0, 0, 255)
    time.sleep(1)
    print("Printing Combinations")
    setLed(255, 255, 0)
    time.sleep(1)
    setLed(0, 255, 255)
    time.sleep(1)
    setLed(255, 0, 255)
    time.sleep(1)
    print("Printing White")
    setLed(255, 255, 255)
    time.sleep(1)
