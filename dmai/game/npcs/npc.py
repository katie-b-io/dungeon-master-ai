
class NPC():
    def __init__(self, npc_data: dict) -> None:
        """Main class for a npc"""
        try:
            for key in npc_data:
                self.__setattr__(key, npc_data[key])

        except AttributeError as e:
            print("Cannot create NPC, incorrect attribute: {e}".format(e=e))
            raise
        
    def __repr__(self) -> str:
        return "NPC: {a}".format(a=self.name)
    