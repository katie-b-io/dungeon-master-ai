from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Race:

    # class variables
    race_data = dict()

    def __init__(self, race: str) -> None:
        """Race class"""
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
            logger.error("Race does not exist: {r}".format(r=e))
            raise
        except AttributeError as e:
            logger.error(
                "Cannot create race, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Race: {r}".format(r=self.name)

    @classmethod
    def _load_race_data(cls) -> None:
        """Set the cls.race_data class variable data"""
        cls.race_data = Loader.load_domain("races")
