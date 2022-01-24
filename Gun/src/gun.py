"""
Gun object that holds the user's state (lives, ammo, team)
"""

# Team 0 = Turret
# Team 1 = Blue gun
# Team 2 = Red gun

import machine
import uasyncio as asyncio

from primitives.pushbutton import Pushbutton


class Gun:
    def __init__(
        self,
        id: int,
        team: int = 1,
        lives: int = 0,
        maxAmmo: int = 0,
        triggerPin: int = 26,
        reloadPin: int = 27,
    ):
        """
        Keep track of players state and handle game mechanics

        team:       Team to which the player belongs. 0=Turret, 1=Blue, 2=Red
        maxAmmo:    Size of a full clip of ammo
        triggerPin: GPIO pin which is pulled LOW on fire
        reloadPin:  GPIO pin which is pulled LOW on reload
        """
        self._id = id
        self._team = team
        self._maxAmmo = maxAmmo

        self._lives = self.lives
        self._ammo = self._maxAmmo

        # Initiating async callbacks to handle button presses
        trigPin = machine.Pin(triggerPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._triggerBtn = Pushbutton(trigPin)
        self._triggerBtn.press_func(self._shoot)

        reloadPin = machine.Pin(reloadPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._reloadBtn = Pushbutton(reloadPin)
        self._reloadBtn.press_func(self._reload)

        # Pre-defined transmit function
        self._transmitCallback = None

        # Flags for game mechanics
        self._shooting = False
        self._reloading = False

    def setTransmitCallback(self, transmitCallback):
        self._transmitCallback = transmitCallback

    async def handleMessage(self, data: int, addr: int):
        print("Handling message")
        if addr < 100:
            self._handleConfiguration(command=addr, value=data)
        elif data != self._team:
            await self._getHit(player=addr, team=data)
        else:
            print("Unexpected message. Addr: " + str(addr) + ", data: " + str(data))

    async def _shoot(self):
        print("Shooting")
        if self._shooting:
            return
        if self._ammo < 1:
            await self._handleOutOfAmmo()
            return

        # TODO Turn on red laser and do buzz
        self._shooting = True
        for i in range(3):  # Transmission takes 67.5ms
            await self._transmitCallback(address=self._id, data=self._team)
        self._ammo -= 1

        print("Done shooting. Ammo: " + str(self._ammo))
        self._shooting = False

    async def _reload(self):
        if self._reloading:
            return

        # Todo: Turn on LED or play sound
        print("Reloading")
        self._reloading = True
        await asyncio.sleep_ms(5000)
        self._ammo = self._maxAmmo
        print("Done reloading. Ammo: " + str(self._ammo))
        self._reloading = False

    async def _getHit(self, player: int, team: int):
        # Handle getting hit
        # TODO: Change LEDS status and play sound or buzz
        print("Got hit by player " + str(player) + " from team " + str(team))
        if self._lives < 1:
            await self._handleDead()
            return

        self._lives -= 1

    async def _handleConfiguration(self, command: int, value: int):
        # Todo Implement LED animatinos for each setting change
        if command == 0:  # Handle setting team
            self._team = value
        elif command == 1:  # Handle setting max ammo
            self._maxAmmo = value
        elif command == 2:  # Handle (re)setting lives
            self._lives = value
        else:
            print(
                "Unexpected special command. Addr: "
                + str(command)
                + ", Data: "
                + str(value)
            )
        print("Handling configuration change")

    async def _handleOutOfAmmo(self):
        # Todo: Play sound or blink LED or something
        print("Out of ammo")

    async def _handleDead(self):
        # Todo: Play sound or blink LED or something
        print("You're dead")
