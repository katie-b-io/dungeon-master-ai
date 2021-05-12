from dmai.domain.characters.character_collection import CharacterCollection
from dmai.game.player import Player
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU
from dmai.dm import DM
from dmai.game.state import State


class Game:
    def __init__(self) -> None:
        """Main class for the game"""
        adventure = "the_tomb_of_baradin_stormfury"
        self.dm = DM(adventure)
        self.intro = True
        self.player = None
        
        # intro text generator
        self.intro_text = self.dm.get_intro_text()

    def input(self, player_utter: str) -> None:
        """Receive a player input"""

        # first check for commands, if we have a command - pause the story telling if necessary
        if player_utter:
            pause = NLU.process_player_command(player_utter)
            if pause:
                State.pause()
                return
            else:
                State.play()
        else:
            if State.paused:
                State.play()

        # the game has started, the introduction is being read, ignore utterances
        if self.intro:
            return

        # the player variable is not set at the beginning of the game
        elif not self.player:
            # player is selecting a class
            if not player_utter:
                return
            player_utter = player_utter.lower()
            char_class = CharacterCollection.get_character(player_utter)
            if char_class:
                self.player = Player(char_class)

        elif not self.player.name:
            # player is entering a name
            self.player.set_name(player_utter)
            succeed = self.dm.input(player_utter, utter_type="name")
        
        elif not State.started:
            # start the game by relaying description of starting room 
            succeed = self.dm.input(player_utter, utter_type="start")

        elif player_utter:
            # attempt to determine the player's intent
            (intent, params) = NLU.process_player_utterance(player_utter)

            # relay the player utterance to the dm
            succeed = self.dm.input(player_utter, intent=intent, kwargs=params)

        return

    def output(self) -> str:
        """Return an output for the player"""

        # the game starts
        if self.intro:
            try:
                State.pause()
                return next(self.intro_text)
            except StopIteration:
                State.play()
                self.intro = False
        
        if State.paused:
            return ""

        # the player variable is not set at the beginning of the game
        if not self.player:
            # get the character options for player
            return NLG.get_char_class()

        elif not self.player.name:
            # get the player's name
            return NLG.get_player_name()

        # get the DM's utterance
        return self.dm.output
