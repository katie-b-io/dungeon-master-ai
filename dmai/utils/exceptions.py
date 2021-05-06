class DiceFormatError(Exception):
    """Raised when the dice format is incorrect"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
