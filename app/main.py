# POSIX standard specification for shell
#  - https://pubs.opengroup.org/onlinepubs/9799919799/
import os

# import sys
import subprocess
import readline

from .tokenizer import tokenize
from .utils import in_path
from .completer import outer_completer
from .constant import builtin_commands, redirect_operators, append_operators
from .commands import handle_echo, handle_type, handle_cd


def handle_commands(input: str, paths: list[str]):
    if input.startswith("echo"):
        handle_echo(input, paths)
    elif input.startswith("pwd"):
        print(os.getcwd())
    elif input.startswith("cd"):
        handle_cd(input, paths)
    elif input.startswith("type"):
        handle_type(input, paths)


def main():
    # mac os uses libedit not GNU readline
    autocomplete_cmd_bind = (
        "bind ^I rl_complete" if readline.backend == "editline" else "tab: complete"
    )

    readline.parse_and_bind(autocomplete_cmd_bind)
    readline.set_completer(outer_completer())

    paths = os.environ["PATH"].split(os.pathsep)

    while True:
        try:
            # sys.stdout.write("$ ")
            user_inp = input("$ ")

            if user_inp.startswith(builtin_commands):
                if user_inp == "exit":
                    break

                handle_commands(user_inp, paths)
            else:
                # Subprocess takes care of executables and os level binaries
                executable = tokenize(user_inp)
                fullpath, path_exist = in_path(executable[0], paths)
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
