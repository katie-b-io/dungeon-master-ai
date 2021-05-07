class DiceFormatError(Exception):
    """Raised when the dice format is incorrect"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class UnrecognisedCommandError(Exception):
    """Raised when the command is unrecognised"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class UnrecognisedEntityError(Exception):
    """Raised when the entity is unrecognised"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
    
    
class UnrecognisedRoomError(Exception):
    """Raised when the room is unrecognised"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"    