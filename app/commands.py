import os

from app.append import append
from app.enum import BackgroundJobStatus
from app.redirection import redirect
from .tokenizer import tokenize

from .utils import in_path
from .constant import (
    builtin_commands,
    redirect_operators,
    append_operators,
    external_paths,
)
from .jobs import bg_job
from .history import cmd_hist


def handle_echo(input: str) -> str:
    args: str = input[5:]

    token_str = ""
    tokens = tokenize(args)
    output = ""

    redirect_operator_found = [token in redirect_operators for token in tokens]
    append_operator_found = [token in append_operators for token in tokens]

    if True in redirect_operator_found:
        output = redirect(tokens, redirect_operator_found)
    elif True in append_operator_found:
        output = append(tokens, append_operator_found)
    else:
        token_str = " ".join(tokens)
        output = token_str

    output = f"{output if {output} else ''}"
    return output


def handle_type(input: str) -> str:
    string_after = input[5:]
    output = ""

    if string_after in builtin_commands:
        output = f"{string_after} is a shell builtin"
    else:
        fullpath, path_exist = in_path(string_after, external_paths)

        if path_exist:
            output = f"{string_after} is {fullpath}"
        else:
            output = f"{string_after}: not found"

    return output


def handle_cd(input: str):
    args: str = input[3:]
    homedir = os.getenv("HOME")
    dir = homedir if args == "~" and homedir else args

    if os.path.exists(dir):
        os.chdir(dir)
    else:
        print(f"cd: {args}: No such file or directory")


def handle_jobs(auto_reaping=False):
    """
    Args:
    auto_reaping: bool
        auto-reaping is a fancy term for calling this function after each command execution
        to check if the any of the job is done. So that we can clean it up.
    """
    if not bg_job.count:
        return
    else:
        for idx, job in enumerate(bg_job.joblist):
            spaces = " ".join(
                ["" for _ in range(0, 24 - (len(job["status"].name) - 1))]
            )
            status = bg_job.update_job_status(idx)

            if auto_reaping:
                if status == BackgroundJobStatus.Done:
                    print(
                        f"[{job['count']}]{job['marker']}  {status.name}{spaces}{job['command']}"
                    )
            else:
                print(
                    f"[{job['count']}]{job['marker']}  {status.name}{spaces}{job['command']}"
                )

        bg_job.clean()


def handle_history(input: str):
    input_list = input.split(" ")

    if "-r" in input_list:
        cmd_hist.append_from_file(input_list[-1])
        return
    elif any("-w" == li or "-a" == li for li in input_list):
        cmd_hist.append_to_file(input_list[-1], "-a" in input_list)
        return

    n = int(input_list[-1].strip()) if len(input_list) > 1 else -1

    hist = cmd_hist.get_all()
    idx = 0

    if n > 0:
        idx = (len(hist) - n) + 1
        hist = cmd_hist.get_lastn(n)

    for cmd in hist:
        print(f"\t{idx} {cmd}")
        idx += 1


def handle_commands(input: str) -> str:
    output = ""

    if input.startswith("echo"):
        output = handle_echo(input)
    elif input.startswith("pwd"):
        print(os.getcwd())
    elif input.startswith("cd"):
        handle_cd(input)
    elif input.startswith("jobs"):
        handle_jobs()
    elif input.startswith("type"):
        output = handle_type(input)
    elif input.startswith("history"):
        handle_history(input)

    return output
