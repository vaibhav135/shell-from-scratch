import os


class CmdHistory:
    def __init__(self):
        self.history = []

        # This basically stores the last index the
        # history append operation, so that when you
        # again perform history -a , we doing it after
        # the last idx
        self.history_append_idx = 0

        self.total_history_file_cmd = 0

        self.history_filepath = os.getenv("HISTFILE", "")

        if self.history_filepath:
            self.append_from_file(self.history_filepath)
            self.total_history_file_cmd = len(self.history)

    def append(self, cmd: str):
        self.history.append(cmd)

    def get_all(self) -> list[str]:
        return self.history

    def get_lastn(self, n: int) -> list[str]:
        hist_len = len(self.history)
        start_idx = hist_len - n
        return self.history[start_idx:hist_len]

    def append_from_file(self, filepath: str):
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                self.history.append(line.strip("\n"))

    def append_to_file(self, filepath: str, is_append_mode: bool = False):
        history = self.history

        if is_append_mode:
            history = self.history[self.history_append_idx :]

        with open(filepath, "a") as file:
            for cmd in history:
                self.history_append_idx += 1
                file.write(cmd + "\n")

    def append_to_histfile(self, filepath: str):
        history = self.history

        if self.total_history_file_cmd:
            history = self.history[self.total_history_file_cmd :]

        with open(filepath, "a") as file:
            for cmd in history:
                file.write(cmd + "\n")


cmd_hist = CmdHistory()
