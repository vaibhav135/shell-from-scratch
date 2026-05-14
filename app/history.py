class CmdHistory:
    def __init__(self):
        self.history = []
        self.history_append_idx = 0

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


cmd_hist = CmdHistory()
