class CmdHistory:
    def __init__(self):
        self.history = []

    def append(self, cmd: str):
        self.history.append(cmd)

    def get_all(self) -> list[str]:
        return self.history

    def get_lastn(self, n: int) -> list[str]:
        hist_len = len(self.history)
        start_idx = hist_len - n
        return self.history[start_idx:hist_len]


cmd_hist = CmdHistory()
