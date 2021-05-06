class TextMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """Text static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Text(metaclass=TextMeta):
    def __init__(self) -> None:
        """Text static class"""
        pass

    @staticmethod
    def yield_text(text: str, delimiter: str = "\n") -> dict:
        """Creates a generator object for splitting text"""
        tokens = text.split(delimiter)
        for token in tokens:
            yield token
