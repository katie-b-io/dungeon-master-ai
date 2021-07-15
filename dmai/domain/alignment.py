from dmai.utils.loader import Loader
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Alignment:

    # class variables
    alignment_data = dict()

    def __init__(self, state: State, alignment: str) -> None:
        """Alignment class"""
        self.state = state
        self.alignment = alignment
        self._load_alignment_data()

        try:
            for key in self.alignment_data[self.alignment]:
                self.__setattr__(key, self.alignment_data[self.alignment][key])

        except KeyError as e:
            logger.error("(SESSION {s}) Alignment does not exist: {c}".format(s=self.state.session.session_id, c=e))
            raise
        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create alignment, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

    def __repr__(self) -> str:
        return "Alignment: {a}".format(a=self.alignment)

    @classmethod
    def _load_alignment_data(cls) -> None:
        """Set the cls.alignment_data class variable data"""
        cls.alignment_data = Loader.load_domain("alignments")
