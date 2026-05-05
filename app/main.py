# POSIX standard specification for shell
#  - https://pubs.opengroup.org/onlinepubs/9799919799/
import os

# import sys
import subprocess
import readline

from app.append import append
from app.redirection import redirect
from .tokenizer import tokenize
from .utils import in_path
from .completer import outer_completer
from .constant import builtin_commands, redirect_operators, append_operators


def handle_commands(input: str, paths: list[str]):
    if input.startswith("echo"):
        args: str = input[5:]

        token_str = ""
        tokens = tokenize(args)

        redirect_operator_found = [token in redirect_operators for token in tokens]
        append_operator_found = [token in append_operators for token in tokens]

        if True in redirect_operator_found:
            redirect(tokens, redirect_operator_found)
        elif True in append_operator_found:
            append(tokens, append_operator_found)
        else:
            token_str = " ".join(tokens)
            print(token_str)
    elif input.startswith("pwd"):
        args: str = input[4:]
        print(os.getcwd())
    elif input.startswith("cd"):
        args: str = input[3:]
        homedir = os.getenv("HOME")
        dir = homedir if args == "~" and homedir else args

        if os.path.exists(dir):
            os.chdir(dir)
        else:
            print(f"cd: {args}: No such file or directory")
    elif input.startswith("type"):
        string_after = input[5:]

        if string_after in builtin_commands:
            print(f"{string_after} is a shell builtin")
        else:
            fullpath, path_exist = in_path(string_after, paths)

            if path_exist:
                print(f"{string_after} is {fullpath}")
            else:
                print(f"{string_after}: not found")


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
