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
    def yield_text(text: str, delimiter: str = "\n") -> str:
        """Creates a generator object for splitting text"""
        tokens = text.split(delimiter)
        for token in tokens:
            yield token

    @staticmethod
    def get_signed_value(value: int) -> str:
        """Method to convert an integer to a signed string"""
        if value > 0:
            value = "+{v}".format(v=value)
        elif value == 0:
            value = " {v}".format(v=value)
        else:
            value = "{v}".format(v=value)
        return value