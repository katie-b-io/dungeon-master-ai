from dmai.game.state import State
from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Race:

    # class variables
    race_data = dict()

    def __init__(self, state: State, race: str) -> None:
        """Race class"""
        self.state = state
        self._load_race_data()

        try:
            for key in self.race_data[race[0]]:
                self.__setattr__(key, self.race_data[race[0]][key])

            if len(race) > 1:
                self.subrace = self.subraces[race[1]]
                self.name = self.subrace["name"]
            else:
                self.subrace = None

        except KeyError as e:
            logger.error("(SESSION {s}) Race does not exist: {r}".format(s=self.state.session.session_id, r=e))
            raise
        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create race, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

    def __repr__(self) -> str:
        return "Race: {r}".format(r=self.name)

    @classmethod
    def _load_race_data(cls) -> None:
        """Set the cls.race_data class variable data"""
        cls.race_data = Loader.load_domain("races")
