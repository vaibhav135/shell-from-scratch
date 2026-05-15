from pathlib import Path

from app.constant import builtin_commands
from app.external_executables import external_exec_list
from app.utils import get_file_and_dir

from .enum import CompletionType


def is_nested_file(path: str) -> bool:

    path_idx = path.rfind("/")
    if path_idx == -1:
        return False

    dir_path = path[: path_idx + 1]
    return Path(dir_path).is_dir() and path_idx + 1 < len(path)


def get_completion_type(line_buffer: str) -> CompletionType:
    completion_type = CompletionType.CommandCompletion
    input = line_buffer.split(" ")

    if input.__len__() > 1:
        path = input[-1]
        path_idx = path.rfind("/")
        is_dir = path_idx > -1

        if is_dir:
            completion_type = CompletionType.NestedDirCompletion
        else:
            completion_type = CompletionType.CurDirCompletion

    return completion_type


def get_completion_list(text: str, completion_type: CompletionType) -> list[str]:
    completion_list = []
    path_idx = text.rfind("/")

    if completion_type == CompletionType.CommandCompletion:
        completion_list = list(builtin_commands) + external_exec_list
    elif completion_type == CompletionType.NestedDirCompletion:
        path = text[: path_idx + 1]
        completion_list = get_file_and_dir(Path(path))
    else:
        completion_list = get_file_and_dir(Path.cwd())

    return completion_list


def get_matches(
    command: list[str], text: str, completion_type: CompletionType
) -> list[str]:
    args = ""

    if len(command) > 1:
        args = command[1]

    # default completion list
    completion_list = get_completion_list(args if args else text, completion_type)

    find_exact_matches = True

    if args and args[-1] == "/":
        find_exact_matches = False

    if find_exact_matches:
        matches = sorted(
            [
                txt + " " if txt[-1] != "/" else txt
                for txt in completion_list
                if txt.startswith(text if text else args) and txt != text
            ]
        )
    else:
        matches = [cl + " " if cl[-1] != "/" else cl for cl in completion_list]

    if len(matches) == 0:
        matches.append(text)

    return matches
