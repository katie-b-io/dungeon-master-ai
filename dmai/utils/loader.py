import json

class LoaderMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs) -> None:
        '''Loader static singleton metaclass'''
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Loader(metaclass=LoaderMeta):
    
    def __init__(self) -> None:
        '''Loader static class'''
        pass
    
    @staticmethod
    def load_json(file: str) -> dict:
        '''Loads a data structure from JSON file'''
        json_data = dict()
        try:
            with open(file, mode='r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print(f"{file} does not exist!")
        
        return json_data