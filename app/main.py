# POSIX standard specification for shell
#  - https://pubs.opengroup.org/onlinepubs/9799919799/

import subprocess
import readline


from .tokenizer import tokenize
from .utils import in_path, is_background_job
from .constant import (
    builtin_commands,
    redirect_operators,
    append_operators,
    external_paths,
)
from .commands import handle_commands, handle_jobs
from .history import cmd_hist
from .jobs import bg_job
from .declare import declare_var

from app.completer.completer import run_completer
from app.pipe import handle_piping


def main():
    # mac os uses libedit not GNU readline
    autocomplete_cmd_bind = (
        "bind ^I rl_complete" if readline.backend == "editline" else "tab: complete"
    )

    readline.parse_and_bind(autocomplete_cmd_bind)
    readline.set_completer(run_completer.completer)

    while True:
        """
        Two types of command
            echo 'hello world'

            echo 'hello wold' | wc

            user_inp  - 2 types
            if user_inp has | (pipes)
            if they have pipe we split it by "|"
            else we put it in 
            

        """
        try:
            user_inp = input("$ ")
            cmd_hist.append(user_inp)

            args = user_inp.split("|")

            # It basically stores the output of the last command used when
            # the input contains a pipe
            proc_cache: subprocess.Popen[str] | None = None
            prev_cmd_ouput = ""

            piped_commands = len(args) > 1

            if "exit" in args:
                history_filepath = cmd_hist.history_filepath
                if history_filepath:
                    cmd_hist.append_to_histfile(history_filepath)

                break

            for index, arg in enumerate(args):
                arg = arg.strip()
                arg_list = arg.split(" ")
                is_last_idx = (index + 1) == len(args)

                if arg.startswith(builtin_commands):
                    prev_cmd_ouput = handle_commands(arg)
                    if (
                        prev_cmd_ouput
                        and (not piped_commands or (piped_commands and is_last_idx))
                        and arg.startswith(("echo", "type"))
                    ):
                        print(prev_cmd_ouput)

                    if arg != "jobs":
                        handle_jobs(auto_reaping=True)

                elif is_background_job(arg):
                    arg_list.remove("&")
                    proc = subprocess.Popen(arg_list)
                    proc.returncode

                    bg_job.add_job(proc=proc, pid=proc.pid, command=arg)
                    print(f"[{bg_job.count}] {proc.pid}")
                elif piped_commands:
                    proc_cache = handle_piping(
                        arg_list, proc_cache, prev_cmd_ouput, is_last_idx
                    )
                    if proc_cache and is_last_idx:
                        stdout, _ = proc_cache.communicate()
                        if stdout:
                            print(stdout, end="")

                else:
                    vars = declare_var.extract_values(arg)
                    # print(f"\ncustom command: {vars}")

                    if len(vars) > 0:
                        executable = []
                        count = 0

                        for a in arg.split(" "):
                            if "$" in a:
                                executable.append(vars[count])
                                count += 1
                            else:
                                executable.append(a)

                        subprocess.run(executable)
                    else:
                        # Subprocess takes care of executables and os level binaries
                        executable = tokenize(arg)
                        fullpath, path_exist = in_path(executable[0], external_paths)
                        operators = redirect_operators + append_operators

                        found_shell_operator = any(
                            operator in executable for operator in operators
                        )

                        if found_shell_operator:
                            # Let the shell handle, stdout, stdin operator
                            subprocess.run(" ".join(executable), shell=True)
                        elif path_exist:
                            subprocess.run(executable)
                        else:
                            print(f"{arg}: command not found")

            proc_cache = None
            prev_cmd_ouput = ""

        except KeyboardInterrupt:
            history_filepath = cmd_hist.history_filepath
            if history_filepath:
                cmd_hist.append_to_histfile(history_filepath)
            return


if __name__ == "__main__":
    main()
