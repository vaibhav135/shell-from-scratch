from pathlib import Path

from app.constant import builtin_commands
from app.external_executables import external_exec_list
from app.utils import files_in_dir

from .enum import CompletionType


def get_completion_type(line_buffer: str) -> CompletionType:
    completion_type = CompletionType.CommandCompletion
    input = line_buffer.split(" ")

    if input.__len__() > 1:
        path = input[1]
        path_idx = path.rfind("/")
        path = "" if path_idx < 0 else path[: path_idx + 1]

        if path and Path(path).is_dir():
            completion_type = CompletionType.NestedFileCompletion
        else:
            completion_type = CompletionType.FileCompletion

    return completion_type


def get_completion_list(text: str, completion_type: CompletionType) -> list[str]:
    completion_list = []

    if completion_type == CompletionType.CommandCompletion:
        completion_list = list(builtin_commands) + external_exec_list
    elif completion_type == CompletionType.NestedFileCompletion:
        path = text[: text.rfind("/") + 1]
        completion_list = files_in_dir(Path(path))
    else:
        completion_list = files_in_dir(Path.cwd())

    return completion_list


def get_matches(
    matches: list[str], text: str, completion_type: CompletionType
) -> list[str]:

    completion_list = get_completion_list(text, completion_type)

    if completion_type == CompletionType.NestedFileCompletion:
        matches = [li + " " for li in completion_list]
    else:
        matches = sorted(
            [
                txt + " "
                for txt in completion_list
                if txt.startswith(text) and txt != text
            ]
        )

    if len(matches) == 0:
        matches.append(text)

    return matches
