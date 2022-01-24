from machine import UART
from machine import Pin


class MotionDetector:

    def __init__(self):
        # UART
        self.uart = UART(1, 9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)

        # Motion detection
        self.interrupt_pin = -1
        self.pirPins = []
        self.motion = False
        self.init_motion_detection()

    def init_motion_detection(self):
        # First four pins next to ground on ESP8266
        pir0 = Pin(2, Pin.IN)
        pir1 = Pin(0, Pin.IN)
        pir2 = Pin(4, Pin.IN)
        pir3 = Pin(5, Pin.IN)
        pir0.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir1.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir2.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir3.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        self.pirPins = [pir0, pir1, pir2, pir3]

    def handle_interrupt_pir(self, pin):
        self.interrupt_pin = self.pirPins.index(pin)
        self.motion = True

    async def detection(self):
        while True:
            if self.motion:
                frame = bytearray([6, self.interrupt_pin])
                self.uart.write(frame)
                print(frame)
                self.motion = False
