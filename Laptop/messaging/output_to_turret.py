"""codeauthor:: Brand Hauser
Class for communicating from the control computer to the microcontroller on the turret.
For passing instructions to the turret.  Uses a Messenger class for modular communication."""
import time

from Laptop.data.values import Status, Direction


class OutputToTurret:
    def __init__(self, pan_messenger, tilt_messenger):
        self.pan_messenger = pan_messenger
        self.tilt_messenger = tilt_messenger

    def pan_send(self, output):
        """Send command over serial port to laser turret.  Used for controlling
        actions of the turret.
        :param output: 3 byte command where byte #1 = opcode & byte #2 = control value """
        self.pan_messenger.send(output)

    def tilt_send(self, output):
        self.tilt_messenger.send(output)

    def tilt_at_speed(self, speed):
        """Turret control command to tilt at a certain speed.
        If speed < 0: turret tilts down.
        If speed > 0: turret tilts up.
        If speed = 0: stop previous tilt command.
        Speed values below 5 will result in stop due to limitation of motor.
        :param speed: int value between -100 and 100, equates to percentage of full speed"""
        self.tilt_send(int.to_bytes(0, 1, 'big') + speed.to_bytes(2, 'big', signed= True))

    def tilt_special(self, command):
        """Turret control command to tilt turret to one of 2 specified positions.
        If command = "offline": Turret tilts down into offline position.
        If command = "ready": turret tilts to level ready position.
        :param command: enum value from data.values.py - Status """
        self.tilt_send(int.to_bytes(1, 1, 'big') + int.to_bytes(command.value, 2, 'big'))

    def pan_at_speed(self, speed):
        """Turret control command to rotate turret at the specified speed.
        If speed < 0: turret rotates left.
        If speed > 0: turret rotates right.
        If speed = 0: stop previous pan command.
        Speed values below 5 will result in stop due to limitation of motor.
        :param speed: int value between -100 and 100, equates to percentage of full speed"""
        self.pan_send(int.to_bytes(2, 1, 'big') + speed.to_bytes(2, 'big', signed= True))

    def pan_relative_angle(self, angle):
        """Turret control command to rotate the turret to the specified angle relative
        to its current position.  Negative angles equate to rotating left.  Positive
        angles equate to rotating right.
        :param angle: the angle to turn from current position"""
        angle = int(angle // 1.8)
        self.pan_send(int.to_bytes(3, 1, 'big') + angle.to_bytes(2, 'big', signed=True))

    def motion_detect_send_direction(self, direction):
        """Turret control command to send the direction at which motion was detected by the motion
        sensors. The turret will move left or right based on this.
        :param direction: enum value from data.values.py - Direction"""
        value = direction.value
        print(value)
        command = int.to_bytes(7, 1, 'big') + int(value).to_bytes(2, 'big', signed=True)
        print(command)
        self.pan_send(command)

    def fire(self):
        """Turret control command to fire laser at current target.  Checks if turret is offline first."""
        self.tilt_send(int.to_bytes(5, 1, 'big') + int.to_bytes(0, 2, 'big'))

