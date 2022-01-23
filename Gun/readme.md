Code that runs on the guns

- Ensure faults are because of simultaneous transmission/reception
- Implement "shooting" feature (few burst with wait in between and afterwards)
- Add lives
- Add reload/life reset point thingies
    - Maybe a team-based ESP8266 that emits to a certain address
- Implement easy programmability on game start (team, ammo, lives)
    - Team using target color of front leds
- Battery indicator
    - https://github.com/LilyGO/LILYGO-T-Energy/issues/7

- Implement score keeping over bluetooth

The absolute maximum current drawn per GPIO is 40mA

Displaying data ideas
- OLED / LCD screen (needs a lot of pins)
- Indicator LEDS (needs multiple pins)
- Bluetooth and phone (need a lot of programming and gun re-design)