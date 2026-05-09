import readline


from .helper import get_completion_type, get_matches


def outer_completer():
    matches = []
    prev_text = ""
    count = 0

    # Text will be empty if it contains any of these delimiters  `~!@#$%^&*()-=+[{]}\|;:'",<>/?
    def completer(text: str, state: int) -> str | None:
        nonlocal matches
        nonlocal prev_text
        nonlocal count

        line_buffer = readline.get_line_buffer()
        command = line_buffer.split(" ")

        completion_type = get_completion_type(line_buffer)

        is_new_text = (
            True if (prev_text or count) and prev_text != command[-1] else False
        )

        if is_new_text:
            matches = []
            prev_text = ""
            count = 0

        try:
            if state == 0:
                if len(matches) > 0 and not is_new_text:
                    if len(command) == 1:
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
                    if text:
                        prev_text = text
                    else:
                        count += 1
                        prev_text = command[-1]
                    matches = get_matches(command, text, completion_type)

            if state > len(matches) or len(matches) == 0:
                return None

            if len(command) > 1 and command[1] and not text:
                """
                    This handles the specific case of a text where dilimiter will be there at the end of the text.
                    
                    for example:
                        du hello-
                        and assume there is a file called du hello-wold.txt.

                    libedit or readline see the dilimiter as word boundary and once you type a character and press TAB
                    it will go back see the delimiter and will get the characters after the delimiter which is why the text
                    will be empty string ("") but worry not we do have line_buffer which give us everything the user
                    typed so far.

                    Returns:
                        rest of the string after the delimit only applicable for files and dir name.

                """
                delimit = command[1][-1]
                delimit_idx = matches[state].rfind(delimit)
                match = matches[state][delimit_idx + 1 :]
                if delimit_idx > -1 and match:
                    return match

            return matches[state]
        except IndexError:
            return None

    return completer
