import random

import uasyncio as asyncio

from gun import Gun
from ir_com import Communicator


async def test(gun):
    print("Starting testing")

    print("########## Setting team")
    await gun.handleMessage(addr=0, data=1)
    await asyncio.sleep(3)

    print("########## Testing reload without ammo")
    await gun._reload()
    await asyncio.sleep(3)

    print("########## Settting maxAmmo")
    await gun.handleMessage(addr=1, data=10)
    await asyncio.sleep(3)

    print("########## Testing reload with ammo")
    await gun._reload()
    await asyncio.sleep(3)

    print("########## Settting lives")
    await gun.handleMessage(addr=2, data=3)
    await asyncio.sleep(3)

    print("########## Shooting")
    await gun._shoot()
    await asyncio.sleep(3)

    print("########## Getting shot by same team")
    await gun.handleMessage(addr=120, data=1)
    await asyncio.sleep(3)

    print("########## Getting shot by different team")
    await gun.handleMessage(addr=120, data=2)
    await asyncio.sleep(3)

    print("Testing done")

async def main():
    userID = random.randint(100, 65535)
    print("UserID: " + str(userID))

    # Initialize gun and communicator
    gun = Gun(id=userID, triggerPin=26, reloadPin=27)
    ir = Communicator(transmitPin=12, receivePin=14)

    # Inject callbacks
    gun.setTransmitCallback(transmitCallback=ir.transmit)
    ir.setMessagehandlerCallback(messageHandler=gun.handleMessage)

    # Forever block to keep async services running
    await test(gun=gun)

    while True:
        await asyncio.sleep(60)
        print("Heartbeat: Program is still running")


import time

time.sleep(3)
print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()
