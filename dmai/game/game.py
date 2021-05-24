from dmai.utils.output_builder import OutputBuilder
from dmai.domain.characters.character_collection import CharacterCollection
from dmai.game.player import Player
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU
from dmai.dm import DM
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Game:
    def __init__(self, char_class: str = None, char_name: str = None, skip_intro: bool = False) -> None:
        """Main class for the game"""
        adventure = "the_tomb_of_baradin_stormfury"
        logger.info("Initialising adventure: {a}".format(a=adventure))
        self.dm = DM(adventure)
        State.set_dm(self.dm)
        self.player = None
        
        # set character class and name if possible
        if char_class:
            character = CharacterCollection.get_character(char_class)
            self.player = Player(character)
            State.set_player(self.player)
        
            if char_name:
                self.player.set_name(char_name)
        
        # intro text generator
        if skip_intro:
            State.pause()
            self.intro = False
            self.intro_text = iter(())
        else:
            self.intro = True
            self.intro_text = self.dm.get_intro_text()
            
    def input(self, player_utter: str) -> None:
        """Receive a player input"""
        
        # clear the output
        OutputBuilder.clear()
        
        # reset the talking state
        if State.talking:
            State.stop_talking()
            
        # first check for commands, if we have a command - pause the story telling if necessary
        if player_utter:
            (pause, player_utter) = NLU.process_player_command(player_utter)
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
            character = CharacterCollection.get_character(player_utter)
            if character:
                self.player = Player(character)
                State.set_player(self.player)

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
            
            if succeed:
                # if succeeded, clear stored intent
                State.clear_intent()
            else:
                # failed, keep track of intent
                State.store_intent(intent, params)

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
            if OutputBuilder.has_response():
                return OutputBuilder.format()
            else:
                return ""

        # the player variable is not set at the beginning of the game
        if not self.player:
            # get the character options for player
            return NLG.get_char_class(CharacterCollection.get_all_names())

        elif not self.player.name:
            # get the player's name
            return NLG.get_player_name()

        # get the DM's utterance
        return self.dm.output
