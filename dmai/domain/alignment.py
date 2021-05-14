from dmai.utils.loader import Loader


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
            print("Alignment does not exist: {c}".format(c=e))
            raise
        except AttributeError as e:
            print("Cannot create alignment, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Alignment: {a}".format(a=self.alignment)

    @classmethod
    def _load_alignment_data(cls) -> None:
        """Set the cls.alignment_data class variable data"""
        cls.alignment_data = Loader.load_json("data/domain/alignments.json")
