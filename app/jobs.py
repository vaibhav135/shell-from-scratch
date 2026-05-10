class BackgroundJob:
    def __init__(self):
        self.joblist = []
        self.count = 0

    def add_job(self, pid: int, command: str):
        self.count += 1
        self.joblist.append({"pid": pid, "count": self.count, "command": command})

    def get_job(self):
        return self.joblist


bg_job = BackgroundJob()
