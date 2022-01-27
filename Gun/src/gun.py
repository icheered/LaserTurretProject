"""
Gun object that holds the user's state (lives, ammo, team)
"""
import time
import machine
import neopixel
import uasyncio as asyncio
from struct import unpack

from primitives.pushbutton import Pushbutton
from turretPeripherals import MotionDetector, SerialCommunicator


class _Gun:
    def __init__(self, id: int, team: int):
        self._id = id
        self._team = team

        self._transmitCallback = None
        self._shooting = False

    def start(self):
        # Doesn't HAVE to be implemented
        pass

    def setTransmitCallback(self, transmitCallback):
        self._transmitCallback = transmitCallback

    async def _handleMessage(self, data: int, addr: int):
        print("Handling message")
        if addr < 100:
            await self._handleConfiguration(command=addr, value=data)
        else:
            await self._getShot(player=addr, team=data)

    async def _shoot(self):
        raise NotImplementedError

    async def _getShot(self, player: int, team: int):
        raise NotImplementedError

    async def _handleConfiguration(self, command: int, value: int):
        # Doesn't have to be implemented for the turret
        pass


class HandGun(_Gun):
    def __init__(
            self,
            id: int,
            triggerPin: int,
            reloadPin: int,
            displayClockPin: int,
            d1data: int,
            d2data: int,
            d3data: int,
            laserPin: int,
            vibratorPin: int,
            rgbledPin: int,
            team: int = 0,
            lives: int = 0,
            maxAmmo: int = 0,
    ):
        super().__init__(id=id, team=team)

        if maxAmmo == 0:
            maxAmmo = 20
        if lives == 0:
            lives = 10
        self._maxAmmo = maxAmmo
        self._lives = lives
        self._ammo = self._maxAmmo

        # self._displayCLKPin = machine.Pin(displayClockPin, machine.Pin.OUT)
        # self._d1dataPin = machine.Pin(d1data, machine.Pin.OUT)
        # self._d2dataPin = machine.Pin(d2data, machine.Pin.OUT)
        # self._d3dataPin = machine.Pin(d3data, machine.Pin.OUT)
        self._laserPin = machine.Pin(laserPin, machine.Pin.OUT)
        self._vibratorPin = machine.Pin(vibratorPin, machine.Pin.OUT)

        trigPin = machine.Pin(triggerPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._triggerBtn = Pushbutton(trigPin)
        self._triggerBtn.press_func(self._shoot)

        reloadPin = machine.Pin(reloadPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._reloadBtn = Pushbutton(reloadPin)
        self._reloadBtn.press_func(self._reload)

        self.neoPixel = neopixel.NeoPixel(machine.Pin(rgbledPin), 8)

        self._brightness = 255
        self._updateTeamColor()

        self._reloading = False
        self._updateDisplays()

    def _updateDisplays(self):
        # Update the 2 ammo displays
        # Update the life display
        pass

    def _updateTeamColor(self):
        if self._team == 0:
            self._set_led(self._brightness, self._brightness, self._brightness) # White
        elif self._team == 1:
            self._set_led(self._brightness, 0, 0) # Red
        elif self._team == 2:
            self._set_led(0, 0, self._brightness) # Blue
        elif self._team == 3:
            self._set_led(0, self._brightness, 0) # Blue
        else:
            print("Team color is not defined")

    def _set_led(self, r, g, b):
        self.neoPixel.fill((r, g, b))
        self.neoPixel.write()

    async def _doVibration(self, duration):
        self._vibratorPin.value(1)
        await asyncio.sleep(duration)
        self._vibratorPin.value(0)

    async def _doLaser(self, duration):
        self._laserPin.value(1)
        await asyncio.sleep(duration)
        self._laserPin.value(0)

    async def _shoot(self):
        print("Shooting")
        if self._shooting:
            return
        if self._ammo < 1:
            await self._handleOutOfAmmo()
            return
        if self._lives < 1:
            await self._handleDead()
            return
        asyncio.create_task(self._doVibration(0.2))
        asyncio.create_task(self._doLaser(0.5))
        self._shooting = True
        for i in range(3):  # Transmission takes 67.5ms
            await self._transmitCallback(address=self._id, data=self._team)
        self._ammo -= 1
        self._updateDisplays()
        print("Done shooting. Ammo: " + str(self._ammo))
        self._shooting = False

    async def _reload(self):
        if self._reloading:
            return

        print("Reloading")
        self._reloading = True
        for i in range(4):
            await self._doVibration(0.5)
            await asyncio.sleep_ms(500)

        for i in range(5):
            await self._doVibration(0.1)
            await asyncio.sleep_ms(100)

        self._ammo = self._maxAmmo
        self._updateDisplays()
        print("Done reloading. Ammo: " + str(self._ammo))
        self._reloading = False

    async def _getShot(self, player: int, team: int):
        # Handle getting hit
        print("Got hit by player " + str(player) + " from team " + str(team))
        if team == self._team and team != 0:
            print("Got hit by same team, ignoring")
            return

        if self._lives < 1:
            await self._handleDead()
            return

        self._lives -= 1
        self._updateDisplays()
        await self._doVibration(2)
        print("Lives: " + str(self._lives))

    async def _handleConfiguration(self, command: int, value: int):
        print("Handling configuration change")
        if command == 0:  # Handle setting team
            self._team = value
            print("Team set to: " + str(self._team))
            self._updateTeamColor()
        elif command == 1:  # Handle setting max ammo
            self._maxAmmo = value
            print("Max ammo set to: " + str(self._maxAmmo))
        elif command == 2:  # Handle (re)setting lives
            self._lives = value
            print("Lives set to: " + str(self._lives))
            self._updateDisplays()
        elif command == 3: # Handle setting LED brightness
            self._brightness = value
            self._updateTeamColor()
        else:
            print(
                "Unexpected special command. Addr: "
                + str(command)
                + ", Data: "
                + str(value)
            )

    async def _handleOutOfAmmo(self):
        # TODO Play sound or blink LED or something
        print("Out of ammo")

    async def _handleDead(self):
        print("You're dead")
        await self._doVibration(10)


class Turret(_Gun):
    def __init__(self, id: int, motionPins: list, team: int = 0):
        super().__init__(id=id, team=team)
        # Instantiate peripherals
        self._motionDetector = MotionDetector(motionDetectorPins=motionPins)
        self._serialCom = SerialCommunicator()

        # Inject callback functions
        self._serialCom.setHandlerCallback(self._handleSerialInput)
        self._motionDetector.setSendSerialCallback(self._serialCom.send)

    def start(self):
        # Initiate background functions
        print("Starting serial com and motiondetector")
        asyncio.create_task(self._serialCom.doReceive())
        asyncio.create_task(self._motionDetector.doDetection())

    async def _handleSerialInput(self, opcode, message):
        print("Receiving serial input")
        print("Opcode: " + str(opcode) + ", Message: " + str(message))
        if opcode[0] == 5:  # SHOOT
            await self._shoot()

    async def _shoot(self):
        print("Shooting")
        if self._shooting:
            return

        self._shooting = True
        for i in range(3):  # Transmission takes 67.5ms
            await self._transmitCallback(address=self._id, data=self._team)

        print("Done shooting")
        self._shooting = False

    async def _getShot(self, player: int, team: int):
        print("Got shot by player: " + str(player) + ", of team: " + str(team))
        self._serialCom.send(opcode=7, data=1)
