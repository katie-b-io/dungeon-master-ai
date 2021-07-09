import textwrap

from dmai.utils.text import Text


class OutputBuilder():

    def __init__(self) -> None:
        """self.output_builder static class"""
        self.output_utterances = []

    def clear(self) -> None:
        """Clear the output"""
        self.output_utterances = []

    def append(self, utterance: str, wrap: bool = False, newline: bool = False) -> None:
        """Append an utterance to the output"""
        if utterance:
            if wrap:
                self.output_utterances.extend(
                    textwrap.wrap(utterance, 100, replace_whitespace=False)
                )
            else:
                self.output_utterances.append(utterance)
            self.output_utterances.append("")

    def format(self) -> str:
        """Return the formatted output"""
        return Text.properly_format_list(
            self.output_utterances, delimiter="\n", last_delimiter="\n"
        )

    def print(self) -> str:
        """Print the formatted output"""
        print(self.format())

    def has_response(self) -> bool:
        """Return whether the DM has a response"""
        return len(self.output_utterances) > 0
