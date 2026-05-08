import readline

from .helper import get_completion_type, get_matches


def outer_completer():
    matches = []
    prev_text = ""

    def completer(text: str, state: int) -> str | None:
        nonlocal matches
        nonlocal prev_text

        line_buffer = readline.get_line_buffer()

        if not len(text.strip()):
            text = line_buffer.split(" ")[1]

        completion_type = get_completion_type(line_buffer)
        is_new_TAB = True if prev_text and prev_text != text else False

        try:
            if state == 0:
                if len(matches) > 0 and not is_new_TAB:
                    """
                    This is handling the second tab press. I have to manually print all the
                    values, otherwise the default string fortmatting won't pass codecrafters
                    tests



                    Why do it like this? 

                        Usually you wouldn't! You would just use the completeion display hook
                        from gnureadline. But macos sucks and don't support gnureadline. That's why I
                        am stuck with this kind of hacky solutions.

                    """

                    print()
                    match_string = " ".join(matches)
                    print(f"{match_string}")
                    print(f"$ {text}")

                    # Reset the nonlocal variables
                    matches = []
                    prev_text = ""

                    return None
                else:
                    prev_text = text
                    matches = get_matches(matches, text, completion_type)

            if state > len(matches):
                return None

            return matches[state]
        except IndexError:
            return None

    return completer
