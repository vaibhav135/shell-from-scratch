import readline
from .constant import builtin_commands
from .external_executables import external_exec_list


def outer_completer():
    matches = []

    def completer(text: str, state: int) -> str | None:
        nonlocal matches

        try:
            if state == 0:
                if len(matches) > 0:
                    """
                    This is handling the second tab press


                    Why do it like this? 

                        Usually you wouldn't! You would just use the completeion display hook
                        from gnureadline. But macos sucks and don't support gnureadline. That's why I
                        am stuck with this kind of hacky solutions.
                    """
                    print()
                    match_string = " ".join(matches)
                    print(f"{match_string}")
                    print(f"$ {text}")
                    return None

                matches = sorted(
                    [
                        txt + " "
                        for txt in (list(builtin_commands) + external_exec_list)
                        if txt.startswith(text)
                    ]
                )

                if len(matches) == 0:
                    matches.append(text)

            if state > len(matches):
                return None

            return matches[state]
        except IndexError:
            return None

    return completer


def pre_input_hook():
    print("CHall agay")
    readline.redisplay()
