from dmai.utils.loader import Loader


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
            print("Race does not exist: {r}".format(r=e))
            raise
        except AttributeError as e:
            print("Cannot create race, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Race: {r}".format(r=self.name)

    @classmethod
    def _load_race_data(self) -> None:
        """Set the self.race_data class variable data"""
        self.race_data = Loader.load_json("data/races.json")
