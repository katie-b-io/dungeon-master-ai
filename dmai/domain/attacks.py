from dmai.utils.loader import Loader


class Attacks:

    # class variables
    attack_data = dict()

    def __init__(self, attacks: dict = {}) -> None:
        """Attacks class"""
        self.attacks = attacks
        self._load_attack_data()

    def __repr__(self) -> str:
        return "Attacks:\n{a}".format(a=self.attacks)

    @classmethod
    def _load_attack_data(cls) -> None:
        """Set the cls.attack_data class variable data"""
        cls.attack_data = Loader.load_domain("attacks")

    def get_all_attack_ids(self) -> list:
        """Method to return all attack IDs"""
        return self.attacks.keys()

    def get_attack(self, attack_id: str) -> dict:
        """Method to get specified attack.
        Returns dict."""
        try:
            return self.attacks[attack_id]
        except KeyError:
            msg = "Attack not recognised: {a}".format(a=attack_id)
            raise KeyError(msg)
