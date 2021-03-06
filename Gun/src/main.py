import random
import time

import machine
import uasyncio as asyncio

from gun import HandGun, Turret
from ir_com import Communicator
from turretPeripherals import SerialCommunicator

# Pin definitions
TURRET = 23  # If tied to ground ESP is turret, else Handgun
TRIGGER = 33  # Shooting      (Handgun only)
RELOAD = 35  # Reloading     (Handgun only)
MOTION = [32, 33, 34, 35]  # Motion detection          (Turret only)
TRANSMIT = 4  # IR Tranmitter pin
RECEIVE = 0  # IR Receiver pin
LASER = 15  # Laser diode
VIBRATOR = 32  # Vibration motor
RGBLED = 2  # RGB LED
SCREENSDA = 25  # LCD Display data line
SCREENSCL = 26  # LCD Display clock line


async def main():
    userID = random.randint(100, 65535)
    print("UserID: " + str(userID))

    # Initialize gun and communicator
    turretPin = machine.Pin(TURRET, machine.Pin.IN, machine.Pin.PULL_UP)
    gun = None
    if turretPin.value():
        print("Creating handgun")
        gun = HandGun(
            id=userID,
            triggerPin=TRIGGER,
            reloadPin=RELOAD,
            laserPin=LASER,
            vibratorPin=VIBRATOR,
            rgbledPin=RGBLED,
            screenSCL=SCREENSCL,
            screenSDA=SCREENSDA,
        )
    else:
        print("Creating turret")
        gun = Turret(id=userID, motionPins=MOTION)

    print("Creating IR communicator")
    ir = Communicator(transmitPin=TRANSMIT, receivePin=RECEIVE)

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


time.sleep(1)
print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()
