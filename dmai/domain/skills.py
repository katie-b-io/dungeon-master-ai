from dmai.utils import Loader

class Skills():
    
    # class variables
    skill_data = dict()
    
    def __init__(self, skills: dict) -> None:
        '''Skills class'''
        self.skills = skills
        self._load_skill_data()
        
    def __str__(self) -> str:
        return "Skills:\n{a}".format(a=self.skills)
    
    @classmethod
    def _load_skill_data(self) -> None:
        '''Set the self.skill_data class variable data'''
        self.skill_data = Loader.load_json("data/skills.json")
        