from pathlib import Path

from app.constant import builtin_commands
from app.external_executables import external_exec_list
from app.utils import get_file_and_dir, get_dir

from .enum import CompletionType, CommandType


def is_nested_file(path: str) -> bool:

    path_idx = path.rfind("/")
    if path_idx == -1:
        return False

    dir_path = path[: path_idx + 1]
    return Path(dir_path).is_dir() and path_idx + 1 < len(path)


def is_dir(path: str) -> bool:
    """
    We are basically check here if we find '/' in the end
    of the path string, if we do meaning it's a dir. Second
    we check if it's legit one by using is_dir and check if
    it exist in our current working directory.
    """
    path_idx = path.rfind("/")

    if path_idx == -1:
        dir = get_dir(Path.cwd())
        return any([path in d for d in dir])

    dir_path = path[: path_idx + 1]
    return Path(dir_path).is_dir() and path_idx + 1 == len(path)


def get_completion_type(line_buffer: str) -> CompletionType:
    completion_type = CompletionType.CommandCompletion
    input = line_buffer.split(" ")

    if input.__len__() > 1:
        command = input[0]
        path = input[1]

        command_type = CommandType.get_command_type(command)

        if command_type == CommandType.BothFileAndDir:
            completion_type = CompletionType.BothDirAndFileCompletion
        elif is_nested_file(path):
            completion_type = CompletionType.NestedFileCompletion
        elif is_dir(path):
            completion_type = CompletionType.DirectoryCompletion
        else:
            completion_type = CompletionType.FileCompletion

    return completion_type


def get_completion_list(text: str, completion_type: CompletionType) -> list[str]:
    completion_list = []
    path_idx = text.rfind("/")

    if completion_type == CompletionType.CommandCompletion:
        completion_list = list(builtin_commands) + external_exec_list
    elif path_idx > -1:
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

    completion_list = get_completion_list(args if args else text, completion_type)

    find_exact_matches = True

    if command and (command[-1] == "/" or len(command) > 1):
        find_exact_matches = False

    if find_exact_matches:
        matches = sorted(
            [
                txt + " "
                for txt in completion_list
                if txt.startswith(text if text else args) and txt != text
            ]
        )
    else:
        matches = [cl + " " if cl[-1] != "/" else cl for cl in completion_list]

    if len(matches) == 0:
        matches.append(text)

    return matches
