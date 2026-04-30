from enum import Enum, auto

from .custom_exceptions import QuoteException


class State(Enum):
    DEFAULT = auto()
    IN_SINGLE_QUOTE = auto()
    IN_DOUBLE_QUOTE = auto()


def tokenize(line: str) -> list[str]:
    line = line.strip()

    if len(line) <= 0:
        return []

    lexemes: list[str] = []
    lexeme = ""

    state = State.DEFAULT
    quote_ended = False

    for char in line:
        match state:
            case State.DEFAULT:
                if char == "'":
                    state = State.IN_SINGLE_QUOTE
                elif char == '"':
                    state = State.IN_DOUBLE_QUOTE
                elif char == " ":
                    if not lexeme and not quote_ended:
                        continue

                    lexemes.append(lexeme)
                    lexeme = ""
                    quote_ended = False
                else:
                    lexeme += char
            case State.IN_SINGLE_QUOTE:
                if char == "'":
                    state = State.DEFAULT
                    quote_ended = True
                else:
                    lexeme += char
            case State.IN_DOUBLE_QUOTE:
                if char == '"':
                    state = State.DEFAULT
                    quote_ended = True
                else:
                    lexeme += char

    if state != State.DEFAULT:
        raise QuoteException("quotes are not closed properly")

    lexemes.append(lexeme)

    return lexemes
