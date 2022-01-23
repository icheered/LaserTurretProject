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
        team: int = 1,
        maxLives: int = 3,
        maxAmmo: int = 10,
        triggerPin: int = 26,
        reloadPin: int = 27,
    ):
        """
        Keep track of players state and handle game mechanics

        team:       Team to which the player belongs. 0=Turret, 1=Blue, 2=Red
        maxLives:   Number of lives a player starts with
        maxAmmo:    Size of a full clip of ammo
        triggerPin: GPIO pin which is pulled LOW on fire
        reloadPin:  GPIO pin which is pulled LOW on reload
        """
        self._team = team
        self._maxLives = maxLives
        self._maxAmmo = maxAmmo

        self._lives = self._maxLives
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

    def handleMessage(self, data, addr):
        print("Handling message")
        print(message)

    async def _shoot(self):
        print("Shooting")
        if self._shooting:
            return
        if self._ammo < 1:
            await self._handleOutOfAmmo()
            return

        # TODO Turn on red laser and do buzz
        self._shooting = True
        for i in range(5):
            await self._transmitCallback(address=self._team, data=10)
            await asyncio.sleep_ms(10)

        self._ammo -= 1

        print("Done shooting. Ammo: " + str(self._ammo))
        self._shooting = False

    async def _reload(self):
        # Handle reloading
        if self._reloading:
            return

        # Todo: Turn on LED or play sound
        print("Reloading")
        self._reloading = True
        await asyncio.sleep_ms(5000)
        self._ammo = self._maxAmmo
        print("Done reloading. Ammo: " + str(self._ammo))
        self._reloading = False

    async def _getHit(self):
        # Handle getting hit
        # TODO: Change LEDS status and play sound or buzz
        print("Get hit")
        if self._lives < 1:
            await self._handleDead()
            return

        self._lives -= 1

    async def _handleConfiguration(self):
        # Handle setting team
        # Handle setting max ammo
        # Handle setting max lives
        # Handle resetting lives
        print("Handling configuration change")

    async def _handleOutOfAmmo(self):
        # Play sound or blink LED or something
        print("Out of ammo")

    async def _handleDaed(self):
        # Play sound or blink LED or something
        print("You're dead")
