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
                 adventure: str = "the_tomb_of_baradin_stormfury",
                 session_id: str = "",
                 saved_state: dict = None) -> None:
        """Main class for the game"""
        self.char_class = char_class
        self.char_name = char_name
        self.skip_intro = skip_intro
        self.adventure = adventure
        self.session_id = session_id
        self.output_builder = OutputBuilder()
        # Initialise state
        self.state = State(self.output_builder, self.session_id)
        if saved_state:
            self.state.load(saved_state)

    def load(self) -> None:
        logger.info("(SESSION: {s}) Initialising adventure: {a}".format(s=self.session_id, a=self.adventure))
        self.player = None

        # Configure endpoints
        RasaAdapter.configure_endpoint()
        
        # load data in static classes
        CharacterCollection.load()
        MonsterCollection.load()

        # Initialise NLU
        self.nlu = NLU(self.state, self.output_builder)

        # Initialise DM
        self.dm = DM(self.adventure, self.state, self.output_builder)
        self.dm.load()
        self.state.set_dm(self.dm)

        # set character class and name if possible
        if not self.char_class and self.state.char_class:
            self.char_class = self.state.char_class
        if not self.char_name and self.state.char_name:
            self.char_name = self.state.char_name
        
        if self.char_class:
            character = CharacterCollection.get_character(self.char_class, self.state, self.output_builder)
            self.player = Player(character, self.state, self.output_builder)
            self.state.set_player(self.player)

            if self.char_name:
                self.state.start()
                if not self.state.char_name:
                    self.state.set_char_name(self.char_name)

        # intro text
        if self.skip_intro or self.state.intro_read:
            self.intro = False
            self.intro_text = ""
        else:
            self.intro = True
            self.intro_text = self.dm.get_intro_text()
            self.state.pause()

    def input(self, player_utter: str) -> None:
        """Receive a player input"""

        # clear the output
        self.output_builder.clear()

        # reset the talking state
        if self.state.talking:
            self.state.stop_talking()

        # the game has started, the introduction is being read, ignore utterances
        if self.intro:
            return

        # the player variable is not set at the beginning of the game
        elif not self.player:
            # player is selecting a class
            if not player_utter:
                return
            player_utter = player_utter.lower()
            character = CharacterCollection.get_character(player_utter, self.state, self.output_builder)
            if character:
                self.state.set_char_class(character)
                self.player = Player(character, self.state, self.output_builder)
                self.state.set_player(self.player)

        elif not self.state.char_name:
            # player is entering a name
            self.state.set_char_name(player_utter)
            succeed = self.dm.input(player_utter, utter_type="name")

        elif player_utter:
            # attempt to determine the player's intent
            player_utter = player_utter.replace("\"", "'")
            (intent, params) = self.nlu.process_player_utterance(player_utter)

            # relay the player utterance to the dm
            succeed = self.dm.input(player_utter, intent=intent, kwargs=params)

            # store intent for next turn
            self.state.store_intent(intent, params)
        
        elif self.state.in_combat or self.state.in_combat_with_door:
            # proceed with combat
            succeed = self.dm.input(player_utter, intent="roll", kwargs={"nlu_entities":[]})

        return

    def output(self) -> str:
        """Return an output for the player"""

        # the game starts
        if self.intro:
            self.intro = False
            self.state.skip_intro()
            if self.player and self.state.char_name:
                self.state.play()
            return self.intro_text

        # the player variable is not set at the beginning of the game
        if not self.player:
            self.state.play()
            # get the character options for player
            return "\n" + NLG.get_char_class(CharacterCollection.get_all_names())

        if not self.state.char_name:
            # get the player's name
            self.state.start()
            self.state.play()
            return "\n" + NLG.get_player_name(self.player.character_class)
        
        # get output ready
        output = ""

        # print welcome text
        if self.output_builder.has_response():
            output = self.output_builder.format()

        elif self.state.paused:
            if self.output_builder.has_response():
                output += "\n" + self.output_builder.format()
            else:
                output += "\n" + ""

        # get the DM's utterance
        else:
            output += "\n" + self.dm.output

        return output
