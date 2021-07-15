import requests

from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class RasaAdapterMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.endpoint = ""
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
    def configure_endpoint(cls) -> None:
        """Method to configure the endpoint"""
        cls.endpoint = "http://{h}:{p}/model/parse".format(
            h=Config.hosts.rasa_host,
            p=Config.hosts.rasa_port
        )

    @classmethod
    def get_intent(cls, player_utter: str) -> tuple:
        """Method which determines player intent from utterance.
        Returns a tuple with the (intent, entities)."""
        try:
            response = cls._parse_message(player_utter)
            intent = response["intent"]["name"]
            confidence = response["intent"]["confidence"]
            entities = cls._prepare_entities(response["entities"])
            return (intent, confidence, entities)
        except ValueError as e:
            logger.error(e)

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
            # not successful, raise error
            msg = "Rasa error: {e}".format(e=r.status_code)
            raise ValueError(msg)

    @classmethod
    def _prepare_entities(self, entities: dict) -> list:
        """Method which converts the Rasa entity object into a generic
        style one for NLU"""
        return_entities = []
        for entity in entities:
            return_entities.append({
                "entity": entity["entity"],
                "value": entity["value"],
                "confidence": entity["confidence_entity"]
            })
        return (return_entities)
