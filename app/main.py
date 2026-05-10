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
from .commands import handle_commands
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

            if user_inp.startswith(builtin_commands):
                if user_inp == "exit":
                    break

                handle_commands(user_inp)
            elif is_background_job(user_inp):
                args = user_inp.split(" ")
                args.remove("&")
                proc = subprocess.Popen(args)

                bg_job.add_job(pid=proc.pid, command=user_inp)
                print(f"[{bg_job.count}] {proc.pid}")
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
