from dmai.utils.loader import Loader
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Alignment:

    # class variables
    alignment_data = dict()

    def __init__(self, alignment: str) -> None:
        """Alignment class"""
        self.alignment = alignment
        self._load_alignment_data()

        try:
            for key in self.alignment_data[self.alignment]:
                self.__setattr__(key, self.alignment_data[self.alignment][key])

        except KeyError as e:
            logger.error("Alignment does not exist: {c}".format(c=e))
            raise
        except AttributeError as e:
            logger.error(
                "Cannot create alignment, incorrect attribute: {e}".format(
                    e=e))
            raise

    def __repr__(self) -> str:
        return "Alignment: {a}".format(a=self.alignment)

    @classmethod
    def _load_alignment_data(cls) -> None:
        """Set the cls.alignment_data class variable data"""
        cls.alignment_data = Loader.load_domain("alignments")
