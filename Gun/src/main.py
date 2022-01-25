import random
import machine
import uasyncio as asyncio

from gun import HandGun, Turret
from ir_com import Communicator

from turretPeripherals import SerialCommunicator

async def main():
    userID = random.randint(100, 65535)
    print("UserID: " + str(userID))

    # Initialize gun and communicator

    # If pin 23 is LOW then this is a turret
    turretPin = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)
    gun = None
    if turretPin.value():
        print("Creating handgun")
        #gun = HandGun(id=userID, triggerPin=26, reloadPin=27)
        gun = HandGun(id=userID, triggerPin=26, reloadPin=27, lives=3, maxAmmo=10)
    else:
        print("Creating turret")
        gun = Turret(id=userID, motionPins=[1, 2, 3, 4], pwmTiltPin=25)  # TODO fix these pins
    
    print("Creating IR communicator")
    ir = Communicator(transmitPin=12, receivePin=14)

    # Inject callbacks
    print("Injecting callbacks")
    gun.setTransmitCallback(transmitCallback=ir.transmit)
    ir.setMessagehandlerCallback(messageHandler=gun._handleMessage)

    print("Starting gun")
    # Start the gun
    gun.start()


    # Forever block to keep async services running
    while True:
        await asyncio.sleep(60)
        print("Heartbeat: Program is still running")


import time

time.sleep(1.5)
print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()
