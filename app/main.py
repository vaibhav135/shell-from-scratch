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
from app.completer.completer import outer_completer
from .jobs import bg_job


def main():
    # mac os uses libedit not GNU readline
    autocomplete_cmd_bind = (
        "bind ^I rl_complete" if readline.backend == "editline" else "tab: complete"
    )

    readline.parse_and_bind(autocomplete_cmd_bind)
    readline.set_completer(outer_completer())

    while True:
        try:
            user_inp = input("$ ")
            piped_commands = "|" in user_inp

            delim = "|" if piped_commands else " "

            args = user_inp.split(delim)

            if user_inp.startswith(builtin_commands):
                if user_inp == "exit":
                    break

                handle_commands(user_inp)

                if user_inp != "jobs":
                    handle_jobs(auto_reaping=True)
            elif is_background_job(user_inp):
                args.remove("&")
                proc = subprocess.Popen(args)
                proc.returncode

                bg_job.add_job(proc=proc, pid=proc.pid, command=user_inp)
                print(f"[{bg_job.count}] {proc.pid}")
            elif piped_commands:
                proc_cache = None
                for arg in args:
                    cmd = arg.strip().split(" ")
                    if proc_cache is None:
                        proc_cache = subprocess.Popen(
                            cmd, stdout=subprocess.PIPE, encoding="utf-8"
                        )
                    else:
                        proc_cache = subprocess.Popen(
                            cmd,
                            stdin=proc_cache.stdout,
                            encoding="utf-8",
                        )

                if proc_cache:
                    stdout, _ = proc_cache.communicate()
                    if stdout:
                        print(stdout, end="")

            else:
                # Subprocess takes care of executables and os level binaries
                executable = tokenize(user_inp)
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
                    print(f"{user_inp}: command not found")

        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
