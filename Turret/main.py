from machine import Pin
import uasyncio

# First four pins next to ground on ESP8266
pir0 = Pin(2, Pin.IN)
pir1 = Pin(0, Pin.IN)
pir2 = Pin(4, Pin.IN)
pir3 = Pin(5, Pin.IN)
pirPins = [pir0,pir1,pir2,pir3]

motion = False

def handle_interrupt_pir(pin):
  global motion
  motion = True
  global interrupt_pin
  interrupt_pin = pirPins.index(pin)


pir0.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt_pir)
pir1.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt_pir)
pir2.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt_pir)
pir3.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt_pir)

async def detection():
    global motion
    while True:
        if motion:
            print(interrupt_pin)
            motion = False

async def blink(pin):
    while True:
        pin.on()
        await uasyncio.sleep_ms(1)
        pin.off()
        await uasyncio.sleep_ms(1)

async def main(pin):
    uasyncio.create_task(blink(pin))
    uasyncio.create_task(detection())
    while True:
        await uasyncio.sleep(1)
uasyncio.run(main(Pin(14, Pin.OUT)))
print("Done!")