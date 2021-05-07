from dmai.utils.loader import Loader


class Alignment:

    # class variables
    alignment_data = dict()

    def __init__(self, alignment: str) -> None:
        """Alignment class"""
        self.alignment = alignment
        self._load_alignment_data()

    def __repr__(self) -> str:
        return "Alignment: {a}".format(a=self.alignment)

    @classmethod
    def _load_alignment_data(self) -> None:
        """Set the self.alignment_data class variable data"""
        self.alignment_data = Loader.load_json("data/alignments.json")
