"""
Gun object that holds the user's state (lives, ammo, team)
"""

import machine
import uasyncio as asyncio
from turretPeripherals import MotionDetector, SerialCommunicator, TiltMotor
from primitives.pushbutton import Pushbutton


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
    def __init__(self, 
        id: int,
        triggerPin: int,
        reloadPin: int,
        team: int = 0,
        lives: int = 0,
        maxAmmo: int = 0
    ):
        super().__init__(id=id, team=team)
        
        self._maxAmmo = maxAmmo
        self._lives = lives
        self._ammo = self._maxAmmo

        trigPin = machine.Pin(triggerPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._triggerBtn = Pushbutton(trigPin)
        self._triggerBtn.press_func(self._shoot)

        reloadPin = machine.Pin(reloadPin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._reloadBtn = Pushbutton(reloadPin)
        self._reloadBtn.press_func(self._reload)

        self._reloading = False
    
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

        # TODO: Turn on red laser and do buzz
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

    async def _getShot(self, player: int, team: int):
        # Handle getting hit
        # TODO: Change LEDS status and play sound or buzz
        # TODO: Implement invincibility timeout
        print("Got hit by player " + str(player) + " from team " + str(team))
        if team == self._team and team != 0:
            print("Got hit by same team, ignoring")
            return
        
        if self._lives < 1:
            await self._handleDead()
            return

        self._lives -= 1
        print("Lives: " + str(self._lives))

    async def _handleConfiguration(self, command: int, value: int):
        print("Handling configuration change")
        # TODO: Implement LED animatinos for each setting change
        if command == 0:  # Handle setting team
            self._team = value
            print("Team set to: " + str(self._team))
        elif command == 1:  # Handle setting max ammo
            self._maxAmmo = value
            print("Max ammo set to: " + str(self._maxAmmo))
        elif command == 2:  # Handle (re)setting lives
            self._lives = value
            print("Lives set to: " + str(self._lives))
        else:
            print(
                "Unexpected special command. Addr: "
                + str(command)
                + ", Data: "
                + str(value)
            )
        
    async def _handleOutOfAmmo(self):
        # TODO: Play sound or blink LED or something
        print("Out of ammo")

    async def _handleDead(self):
        # TODO: Play sound or blink LED or something
        print("You're dead")



class Turret(_Gun):
    def __init__(self, id: int, motionPins: list, pwmTiltPin:int, team: int = 0):
        super().__init__(id=id, team=team)

        # Instantiate peripherals
        self._motionDetector = MotionDetector(motionDetectorPins=motionPins)
        self._serialCom = SerialCommunicator()
        self._tiltMotor = TiltMotor(pwmTiltPin=pwmTiltPin)

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
        if opcode[0] == 0: # Tilt_WPM_Opcode
            tiltSpeed = unpack('>h', message)
            self._tiltMotor.setTilt(int(tiltSpeed[0]/4))
        if opcode[0] == 5: # SHOOT
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

