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


class RoomConnectionError(Exception):
    """Raised when rooms are not connected"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

class UnrecognisedEquipment(Exception):
    """Raised when the equipment is unrecognised"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

class UnrecognisedWeapon(Exception):
    """Raised when the weapon is unrecognised"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"