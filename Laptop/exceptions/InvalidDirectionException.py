class InvalidDirectionException(Exception):
    def __init__(self, direction):
        self.message = direction + " is not a valid direction"
        super().__init__(self.message)
