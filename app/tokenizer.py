from enum import Enum, auto

from .custom_exceptions import QuoteException


class State(Enum):
    DEFAULT = auto()
    IN_SINGLE_QUOTE = auto()
    IN_DOUBLE_QUOTE = auto()


def tokenize(line: str) -> list[str]:
    """
    tokenize iterates over the line (char by char) and returns the final lexemes


    Concept:
    Tokenizers/lexer does two things scanning and evaluation / classification
    scanning - literally go through all the characters and fill up our lexeme
                ofcourse there will be some delimiter to break it into multiple
                lexeme. Basically we are creating multiple subsequeneces

    evaluation/classification - Once we get our lexemes we are basically classifying them
                                into categories like identifier, literal, keyword etc.

    """
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
