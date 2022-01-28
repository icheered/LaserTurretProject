from machine import Pin, PWM
import sys
import uasyncio as asyncio
import select


class SerialCommunicator:
    def __init__(self):

        self.p = select.poll()
        self.p.register(sys.stdin)
        self.opcode = bytearray()
        self.message = bytearray()
        self.count = 0

        self._messageHandler = None

    def setHandlerCallback(self, callback):
        self._messageHandler = callback

    def send(self, opcode, data):
        startbyte = 20
        endbyte = 21
        frame = bytearray([startbyte, opcode, data, endbyte])
        print("Writing to serial: " + str(frame))
        sys.stdout.write(frame)

    async def doReceive(self):
        while True:
            if (len(self.p.poll(0)) > 0):
                if self.count < 1:
                    self.opcode += sys.stdin.buffer.read(1)
                else:
                    self.message += sys.stdin.buffer.read(1)
                self.count += 1
            if (self.count > 2):
                await self._messageHandler(opcode=self.opcode, message=self.message)
                self.count = 0
                self.message = bytearray()
                self.opcode = bytearray()
            await asyncio.sleep(0.1)
            
class MotionDetector:
    def __init__(self, motionDetectorPins: list):
        # Initiate pins
        pir0 = Pin(motionDetectorPins[0], Pin.IN)
        pir1 = Pin(motionDetectorPins[1], Pin.IN)
        pir2 = Pin(motionDetectorPins[2], Pin.IN)
        pir3 = Pin(motionDetectorPins[3], Pin.IN)
        pir0.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir1.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir2.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        pir3.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt_pir)
        self.pirPins = [pir0, pir1, pir2, pir3]

        self.interrupt_pin = -1
        self.motion = False

        self.MOTION_DETECTOR_OPCODE = 6

        self._sendSerial = None

    def setSendSerialCallback(self, callback):
        self._sendSerial = callback     

    def handle_interrupt_pir(self, pin):
        self.interrupt_pin = self.pirPins.index(pin)
        self.motion = True

    async def doDetection(self):
        while True:
            if self.motion:
                self._sendSerial(opcode=self.MOTION_DETECTOR_OPCODE, data=self.interrupt_pin)
                self.motion = False
            await asyncio.sleep(0.1)


