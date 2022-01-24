from ir_com import Communicator

import machine
from primitives.pushbutton import Pushbutton

import uasyncio as asyncio
    

async def main():
    ir = Communicator(transmitPin=12, receivePin=14)

    # Random Values
    someAddress = 10
    someData = 0

    async def sendMessage(): 
        print("Sending")
        await ir.transmit(address=someAddress, data=someData)

    # Create a button that waits for an external interrupt
    trigPin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
    triggerBtn = Pushbutton(trigPin)
    triggerBtn.press_func(sendMessage)

    while True:
        await asyncio.sleep(60)
        print("Still running...")
    
    
import time
time.sleep(3)
print("Starting")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()