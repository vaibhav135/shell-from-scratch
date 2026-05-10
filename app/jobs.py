from subprocess import Popen
from typing import TypedDict, is_typeddict
from app.enum import BackgroundJobStatus


class Job(TypedDict):
    pid: int
    count: int
    command: str
    marker: str
    status: BackgroundJobStatus
    proc: Popen


class BackgroundJob:
    def __init__(self):
        self.joblist: list[Job] = []
        self.count = 0

    def _recompute_markers(self):
        itr_count = 0
        for job in reversed(self.joblist):
            if itr_count == 0:
                job["marker"] = "+"
            elif itr_count == 1:
                job["marker"] = "-"
            else:
                job["marker"] = " "

            itr_count += 1

    def add_job(self, proc: Popen[bytes], pid: int, command: str):
        self.count += 1

        for job in self.joblist:
            job["marker"] = "-" if len(self.joblist) == job["count"] else " "

        self.joblist.append(
            {
                "pid": pid,
                "count": self.count,
                "command": command,
                "marker": "+",
                "status": BackgroundJobStatus.Running,
                "proc": proc,
            }
        )

    def get_job(self):
        return self.joblist

    def update_job_status(self, job_idx: int) -> BackgroundJobStatus:
        job = self.joblist[job_idx]
        statuscode = job["proc"].poll()

        if statuscode is not None:
            command = job["command"].split(" ")
            if command[-1] == "&":
                command.remove("&")
            job["command"] = " ".join(command)

            job["status"] = BackgroundJobStatus.Done
        else:
            job["status"] = BackgroundJobStatus.Running

        return job["status"]

    def clean(self):
        self.joblist = [
            job for job in self.joblist if job["status"] == BackgroundJobStatus.Running
        ]
        self._recompute_markers()


bg_job = BackgroundJob()
