from ..data.values import Status, Direction


def send_over_serial(output):
    """Send command over serial port to laser turret.  Used for controlling
    actions of the turret.
    :param output: 3 byte command where byte #1 = opcode & byte #2 = control value """
    pass


def tilt_at_speed(speed):
    """Turret control command to tilt at a certain speed.
    If speed < 0: turret tilts down.
    If speed > 0: turret tilts up.
    If speed = 0: stop previous tilt command.
    Speed values below 5 will result in stop due to limitation of motor.
    :param speed: int value between -100 and 100, equates to percentage of full speed"""
    pass
    # send_over_serial(int.to_bytes(0) + int.to_bytes(speed))


def tilt_special(command):
    """Turret control command to tilt turret to one of 2 specified positions.
    If command = "offline": Turret tilts down into offline position.
    If command = "ready": turret tilts to level ready position.
    :param command: enum value from data.values.py - Status """
    pass
    # send_over_serial(int.to_bytes(1) + int.to_bytes(degrees))


def pan_at_speed(speed):
    """Turret control command to rotate turret at the specified speed.
    If speed < 0: turret rotates left.
    If speed > 0: turret rotates right.
    If speed = 0: stop previous pan command.
    Speed values below 5 will result in stop due to limitation of motor.
    :param speed: int value between -100 and 100, equates to percentage of full speed"""
    pass


def pan_relative_angle(angle):
    """Turret control command to rotate the turret to the specified angle relative
    to its current position.  Negative angles equate to rotating left.  Positive
    angles equate to rotating right.
    :param angle: the angle to turn from current position"""
    pass


def pan_absolute_angle(direction):
    """Turret control command to rotate to the specified angle relative to the preset
    start angle. Start angle = North.  If start angle is 0 then 100 is South, -50 is
    West and 50 is East
    :param direction: enum value from data.values.py - Direction"""
    pass


def fire():
    """Turret control command to fire laser at current target.  Checks if turret is offline first."""
    pass
