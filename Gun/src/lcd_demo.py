"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""

from lcd.i2c_lcd import I2cLcd
import time
from machine import SoftI2C, Pin

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)

i = 0
while True:
    i += 1
    if i > 99:
        i = 0
    lcd.clear()
    lcd.putstr("Ammo: "+str(i)+ " \nLives: 3")
    time.sleep(0.2)
    
