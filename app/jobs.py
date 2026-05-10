class BackgroundJob:
    def __init__(self):
        self.joblist = []
        self.count = 0

    def add_job(self, pid: int, command: str):
        self.count += 1

        for job in self.joblist:
            job["marker"] = "-" if len(self.joblist) == job["count"] else " "

        self.joblist.append(
            {"pid": pid, "count": self.count, "command": command, "marker": "+"}
        )

    def get_job(self):
        return self.joblist


bg_job = BackgroundJob()
