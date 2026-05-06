import os

from app.append import append
from app.redirection import redirect
from .tokenizer import tokenize

from .utils import in_path
from .constant import builtin_commands
from .constant import redirect_operators, append_operators


def handle_echo(input: str, paths: list[str]):
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


def handle_type(input: str, paths: list[str]):
    string_after = input[5:]

    if string_after in builtin_commands:
        print(f"{string_after} is a shell builtin")
    else:
        fullpath, path_exist = in_path(string_after, paths)

        if path_exist:
            print(f"{string_after} is {fullpath}")
        else:
            print(f"{string_after}: not found")


def handle_cd(input: str, paths: list[str]):
    args: str = input[3:]
    homedir = os.getenv("HOME")
    dir = homedir if args == "~" and homedir else args

    if os.path.exists(dir):
        os.chdir(dir)
    else:
        print(f"cd: {args}: No such file or directory")
