import requests


class RasaAdapterMeta(type):
    _instances = {}
    
    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.endpoint = "http://localhost:5005/model/parse"
        return instance
    
    def __call__(cls, *args, **kwargs) -> None:
        """RasaAdapter static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    
class RasaAdapter(metaclass=RasaAdapterMeta):
    
    def __init__(self) -> None:
        """Class which is used for processing inputs and outputs to the 
        Rasa NLU server"""
        pass
    
    @classmethod
    def get_intent(cls, player_utter: str) -> tuple:
        """Method which determines player intent from utterance.
        Returns a tuple with the (intent, entities)."""
        try:
            response = cls._parse_message(player_utter)
            intent = response["intent"]["name"]
            entities = response["entities"]
            return (intent, entities)
        except ValueError as e:
            print(e)
    
    @classmethod
    def _parse_message(cls, message: str) -> str:
        """Method which sends a message to Rasa NLU server.
        Returns a response."""
        data = "{{\"text\":\"{t}\"}}".format(t=message)
        r = requests.post(cls.endpoint, data=data)
        
        if r.status_code == 200:
            # successful request, return response
            return r.json()
        else:
            # not sucessful, raise error
            msg = "Rasa error: {e}".format(e=r.status_code)
            raise ValueError(msg)
