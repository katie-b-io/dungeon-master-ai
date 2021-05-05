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
        "d100": 100,
        "4": "d4",
        "6": "d6",
        "8": "d8",
        "10": "d10",
        "12": "d12",
        "20": "d20",
        "100": "d100"
    }
    
    def __init__(self) -> None:
        '''DiceRoller static class'''
        pass
    
    @classmethod
    def roll_die(cls, die: str) -> int:
        '''Roll singular specified die'''
        die = die.lower()
        try:
            max_val = cls.dice_map[die]
            if type(max_val) == str:
                die = max_val
                max_val = cls.dice_map[max_val]
            val = random.randint(1, max_val)
            print("Rolling {d}... {v}".format(d=die, v=val))
        except KeyError:
            print("Cannot roll die: {d}".format(d=die))
            raise
        
        return val
    
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
            max_val = cls.dice_map[dice_spec["die"]]
            modifier = dice_spec["mod"]
        except (KeyError, TypeError):
            print("Cannot roll dice with spec: {d}".format(d=dice_spec))
            raise
        
        rolls = [random.randint(1, max_val) for _ in dice]
        total_roll = sum(rolls) + modifier
        return total_roll
    
    @classmethod
    def get_max(cls, die: str) -> int:
        return cls.dice_map[die]
