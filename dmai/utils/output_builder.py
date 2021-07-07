import textwrap

from dmai.utils.text import Text


class OutputBuilderMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.output_utterances = []
        return instance

    def __call__(cls, *args, **kwargs) -> None:
        """OutputBuilder static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class OutputBuilder(metaclass=OutputBuilderMeta):

    # class variables
    output_utterances = []

    def __init__(self) -> None:
        """OutputBuilder static class"""
        pass

    @classmethod
    def clear(cls) -> None:
        """Clear the output"""
        cls.output_utterances = []

    @classmethod
    def append(cls, utterance: str, wrap: bool = False, newline: bool = False) -> None:
        """Append an utterance to the output"""
        if utterance:
            if wrap:
                cls.output_utterances.extend(
                    textwrap.wrap(utterance, 100, replace_whitespace=False)
                )
            else:
                cls.output_utterances.append(utterance)
            cls.output_utterances.append("")

    @classmethod
    def format(cls) -> str:
        """Return the formatted output"""
        return Text.properly_format_list(
            cls.output_utterances, delimiter="\n", last_delimiter="\n"
        )

    @classmethod
    def print(cls) -> str:
        """Print the formatted output"""
        print(cls.format())

    @classmethod
    def has_response(cls) -> bool:
        """Return whether the DM has a response"""
        return len(cls.output_utterances) > 0
