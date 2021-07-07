from dmai.utils.output_builder import OutputBuilder
from dmai.domain.characters.character_collection import CharacterCollection
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.game.player import Player
from dmai.nlu.rasa_adapter import RasaAdapter
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU
from dmai.dm import DM
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Game:
    def __init__(self,
                 char_class: str = None,
                 char_name: str = None,
                 skip_intro: bool = False,
                 adventure: str = "the_tomb_of_baradin_stormfury") -> None:
        """Main class for the game"""
        self.char_class = char_class
        self.char_name = char_name
        self.skip_intro = skip_intro
        self.adventure = adventure

    def load(self) -> None:
        logger.info("Initialising adventure: {a}".format(a=self.adventure))
        self.player = None

        # Configure endpoints
        RasaAdapter.configure_endpoint()
        
        # load data in static classes
        CharacterCollection.load()
        MonsterCollection.load()

        # Initialise DM
        self.dm = DM(self.adventure)
        self.dm.load()
        State.set_dm(self.dm)

        # set character class and name if possible
        if self.char_class:
            character = CharacterCollection.get_character(self.char_class)
            self.player = Player(character)
            State.set_player(self.player)

            if self.char_name:
                self.player.set_name(self.char_name)

        # intro text generator
        if self.skip_intro:
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
            State.start()
            succeed = self.dm.input(player_utter, utter_type="name")

        elif player_utter:
            # attempt to determine the player's intent
            player_utter = player_utter.replace("\"", "'")
            (intent, params) = NLU.process_player_utterance(player_utter)

            # relay the player utterance to the dm
            succeed = self.dm.input(player_utter, intent=intent, kwargs=params)

            # store intent for next turn
            State.store_intent(intent, params)
        
        elif State.in_combat or State.in_combat_with_door:
            # proceed with combat
            succeed = self.dm.input(player_utter, intent="roll", kwargs={"nlu_entities":[]})

        return

    def output(self) -> str:
        """Return an output for the player"""

        # print welcome text
        if OutputBuilder.has_response():
                return OutputBuilder.format()
        
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
