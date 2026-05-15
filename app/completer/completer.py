import readline
import subprocess


from .helper import get_completion_type, get_matches


class Completer:
    def __init__(self):
        self.initialize()
        # list of tuple (command, filepath)
        self.custom_completer_filepath = {}
        self.custom_completer = {}  # store list of completion candidates {"docker": ["run", "compose"] ...}

    def initialize(self):
        self.matches = []
        self.prev_text = ""
        self.count = 0

    def add_custom_completer_file_path(self, cmd: str, filepath: str):
        self.custom_completer_filepath[cmd] = filepath

    def get_custom_completer_candidates(self, cmd: str, args: list) -> list[str]:
        filepath = self.custom_completer_filepath[cmd]
        exec = [filepath]

        if ".py" in filepath:
            exec = ["python3", filepath]

        if len(args) == 3:
            exec.extend(args)

        result = subprocess.run(exec, capture_output=True, text=True)
        completer_candidates = []

        if result.stdout:
            # self.custom_completer[cmd] = [result.stdout.strip() + " "]
            # completer_candidates = self.custom_completer.get(cmd)

            completer_candidates = [result.stdout.strip() + " "]

        return completer_candidates

    # Text will be empty or missing till, if it contains any of these delimiters  `~!@#$%^&*()-=+[{]}\|;:'",<>/?
    def completer(self, text: str, state: int) -> str | None:

        line_buffer = readline.get_line_buffer()
        command = line_buffer.split(" ")

        is_new_text = (
            True
            if (self.prev_text or self.count) and self.prev_text != command[-1]
            else False
        )

        if is_new_text:
            # re-initialize or resetting here
            self.initialize()

        try:
            if state == 0:
                if len(self.matches) > 0 and not is_new_text:
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
                    match_string = " ".join(self.matches)
                    print(f"{match_string}")
                    print(f"$ {line_buffer}", end="")

                    # Reset the nonlocal variables
                    self.matches = []
                    self.prev_text = ""

                    return None
                else:
                    if text:
                        self.prev_text = text
                    else:
                        self.count += 1
                        self.prev_text = command[-1]

                    if any(
                        command[0].strip() == custom_completion_cmd
                        for custom_completion_cmd in self.custom_completer_filepath.keys()
                    ):
                        """
                            argv[1] — The command name being completed (e.g., git)
                            argv[2] — The word currently being completed (the partial text at the cursor)
                            argv[3] — The word immediately before the word being completed. If there's no preceding word, pass an empty string.
                        """
                        args = []

                        if len(command) == 3:
                            args = [command[0], command[-1], command[1]]
                        self.matches = self.get_custom_completer_candidates(
                            command[0].strip(), args
                        )

                        if len(self.matches) == 0:
                            # ring bell for empty matches
                            print("\x07")
                            return None
                    else:
                        completion_type = get_completion_type(line_buffer)
                        self.matches = get_matches(command, text, completion_type)

            if state >= len(self.matches) or len(self.matches) == 0:
                return None

            if len(command) > 1 and command[1] and not text:
                """
                    This handles the specific case of a text where delimiter will be there at the end of the text.
                    
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
                delimit_idx = self.matches[state].rfind(delimit)
                match = self.matches[state][delimit_idx + 1 :]
                if delimit_idx > -1 and match:
                    return match

            return self.matches[state]
        except IndexError:
            return None


run_completer = Completer()
