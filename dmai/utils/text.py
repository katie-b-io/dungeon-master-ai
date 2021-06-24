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

    @staticmethod
    def properly_format_list(
        values: list, delimiter: str = ", ", last_delimiter: str = " and "
    ) -> str:
        """Method to format a list as a proper delimited string"""
        values_str = ""
        if len(values) == 1:
            values_str = "{v}".format(v=values[0])
        elif len(values) > 1:
            values_str = "{a}".format(a=delimiter.join(values[0:-1]))
            values_str += "{l}{a}".format(l=last_delimiter, a=values[-1])
        return values_str
