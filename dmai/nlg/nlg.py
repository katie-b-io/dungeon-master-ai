import random

class NLGMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs) -> None:
        '''NLG static singleton metaclass'''
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class NLG(metaclass=NLGMeta):
    
    # class variable
    game = None
    
    def __init__(self) -> None:
        '''NLG static class'''
        pass
    
    @classmethod
    def set_game(cls, game) -> None:
        cls.game = game
    
    @classmethod
    def get_char_class(cls) -> str:
        '''Return utterance for character selection'''
        c = "\n".join(cls.game.dm.domain.characters.get_all_names())
        utters = [
            "Which character class would you like to play?\n{c}".format(c=c),
            "Select a character class you like the sound of:\n{c}".format(c=c),
            "Select a character class from the following choices:\n{c}".format(c=c)
        ]
        return random.choice(utters)
    
    @classmethod
    def get_player_name(cls) -> str:
        '''Return the utterance for getting player's name'''
        c = cls.game.player.character_class
        utters = [
            "What is your character's name, this great {c}?".format(c=c),
            "Ahh, a {c}. Excellent choice! And what is your character's name?".format(c=c),
            "A {c}, marvelous! And what do they call your character?".format(c=c)
        ]
        return random.choice(utters)
    
    @classmethod
    def get_action(cls) -> str:
        '''Return the utterance for getting a player action'''
        n = cls.game.player.name
        utters = [
            "{n}, what do you do?".format(n=n)
        ]
        return random.choice(utters)
    
    @classmethod
    def get_title(cls) -> str:
        '''Return the utterance for introducing the adventure title'''
        t = cls.game.dm.adventure.title
        utters = [
            "Welcome adventurer, today we're going to play {t}! Let me set the scene...".format(t=t),
            "Today we'll play {t}, an exciting tale of adventure! Let me set the scene...".format(t=t),
            "The title of the adventure we're about to play is: {t}. Let me set the scene...".format(t=t)
        ]
        return random.choice(utters)
    
    @classmethod
    def acknowledge_name(cls) -> str:
        '''Return the utterance for acknowledging player's name'''
        n = cls.game.player.name
        utters = [
            "{n}, simply majestic!".format(n=n),
            "{n}, the finest name in all the lands!".format(n=n),
            "{n}, that's a good one!".format(n=n)
        ]
        return random.choice(utters)
