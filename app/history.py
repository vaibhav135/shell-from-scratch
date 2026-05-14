class CmdHistory:
    def __init__(self):
        self.history = []

    def append(self, cmd: str):
        self.history.append(cmd)

    def get_list(self) -> list[str]:
        return self.history


cmd_hist = CmdHistory()
