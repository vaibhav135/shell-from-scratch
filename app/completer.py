from .constant import builtin_commands
from .external_executables import external_exec_list


def outer_completer():
    possibilities = []

    def completer(text: str, state: int) -> str | None:
        nonlocal possibilities

        try:
            if state == 0:
                possibilities = [
                    txt + " "
                    for txt in (list(builtin_commands) + external_exec_list)
                    if txt.startswith(text)
                ]
                if len(possibilities) == 0:
                    possibilities.append(text)

            if state > len(possibilities):
                return None

            return possibilities[state]
        except IndexError:
            return None

    return completer
