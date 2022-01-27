import random
import time

import machine
import uasyncio as asyncio

from gun import HandGun, Turret
from ir_com import Communicator
from turretPeripherals import SerialCommunicator

# Pin definitions
TURRET = 23  # If tied to ground ESP is turret, else Handgun
TRIGGER = 26  # Shooting      (Handgun only)
RELOAD = 27  # Reloading     (Handgun only)
MOTION = [15, 2, 0, 4]  # Motion detection          (Turret only)
TILT = 25  # Tilt motor control pin    (Turret only)
TRANSMIT = 12  # IR Tranmitter pin
RECEIVE = 14  # IR Receiver pin
DISPLAY_CLK = 13  # Clock pulse for shift registers
DISPLAY1_DATA = 33  # Datapin for shift register display 1
DISPLAY2_DATA = 32  # Datapin for shift register display 2
DISPLAY3_DATA = 35  # Datapin for shift register display 3
LASER = 16  # Laser diode
VIBRATOR = 17  # Vibration motor
RGBLED = 18 # RGB LED


async def main():
    userID = random.randint(100, 65535)
    #print("UserID: " + str(userID))

    # Initialize gun and communicator
    turretPin = machine.Pin(TURRET, machine.Pin.IN, machine.Pin.PULL_UP)
    gun = None
    if turretPin.value():
        #print("Creating handgun")
        gun = HandGun(
            id=userID,
            triggerPin=TRIGGER,
            reloadPin=RELOAD,
            displayClockPin=DISPLAY_CLK,
            d1data=DISPLAY1_DATA,
            d2data=DISPLAY2_DATA,
            d3data=DISPLAY3_DATA,
            laserPin=LASER,
            vibratorPin=VIBRATOR,
            rgbledPin=RGBLED,
            lives=3,
            maxAmmo=20,
        )
    else:
        #print("Creating turret")
        gun = Turret(id=userID, motionPins=MOTION, pwmTiltPin=TILT)

    #print("Creating IR communicator")
    ir = Communicator(transmitPin=TRANSMIT, receivePin=RECEIVE)

    # Inject callbacks
    #print("Injecting callbacks")
    gun.setTransmitCallback(transmitCallback=ir.transmit)
    ir.setMessagehandlerCallback(messageHandler=gun._handleMessage)

    #print("Starting gun")
    # Start the gun
    gun.start()

    # Forever block to keep async services running
    while True:
        await asyncio.sleep(60)
        #print("Heartbeat: Program is still running")


time.sleep(1)
#print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    #print("Got ctrl-c")
    asyncio.new_event_loop()
