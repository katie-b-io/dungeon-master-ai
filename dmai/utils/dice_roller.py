import random

class DiceRollerMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs) -> None:
        '''DiceRoller static singleton metaclass'''
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DiceRoller(metaclass=DiceRollerMeta):
    
    # class variables
    dice_map = {
        "d4": 4,
        "d6": 6,
        "d8": 8,
        "d10": 10,
        "d12": 12,
        "d20": 20,
        "d100": 100
    }
    
    def __init__(self) -> None:
        '''DiceRoller static class'''
        pass
    
    @classmethod
    def roll_die(cls, die: str) -> int:
        '''Roll singular specified die'''
        die = die.lower()
        try:
            max = cls.dice_map[die]
        except KeyError:
            print("Cannot roll die: {d}".format(d=die))
            raise
        
        return random.randint(1, max)
    
    @classmethod
    def roll_dice(cls, dice_spec: dict) -> int:
        '''Roll dice according to spec in dictionary:\n
        {
            "die": "d4",
            "total": 1,
            "mod": 0
        }
        '''
        try:
            dice = range(dice_spec["total"])
            max = cls.dice_map[dice_spec["die"]]
            modifier = dice_spec["mod"]
        except (KeyError, TypeError):
            print("Cannot roll dice with spec: {d}".format(d=dice_spec))
            raise
        
        rolls = [random.randint(1, max) for _ in dice]
        total_roll = sum(rolls) + modifier
        return total_roll
    
    @classmethod
    def get_max(cls, die: str) -> int:
        return cls.dice_map[die]
