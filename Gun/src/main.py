import uasyncio as asyncio

from gun import Gun
from ir_com import Communicator


async def main():
    # Initialize gun and communicator
    gun = Gun(triggerPin=26, reloadPin=27)
    ir = Communicator(transmitPin=12, receivePin=14)

    # Inject callbacks
    gun.setTransmitCallback(transmitCallback=ir.transmit)
    ir.setMessagehandlerCallback(messageHandler=gun.handleMessage)

    # Forever block to keep async services running
    while True:
        await asyncio.sleep(60)
        print("Heartbeat: Program is still running")


print("Starting")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Got ctrl-c")
    asyncio.new_event_loop()
