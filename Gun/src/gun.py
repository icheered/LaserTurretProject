class Gun:
    def __init__(self):
        self.i = 0
        pass

    async def shoot(self):
        # Send a few pulses
        # Decrement ammo
        pass

    async def getHit(self):
        # Handle getting hit
        # Decrement lives
        # If lives == 0:
        #   Handle dying
        # Else:
        #   Set number of life leds
        pass

    async def reload(self):
        # Handle reloading
        pass

    async def handleConfiguration(self):
        # Handle setting team
        # Handle setting max ammo
        # Handle setting max lives
        # Handle resetting lives
        pass
