from enum import Enum
import readline

from .constant import builtin_commands
from .external_executables import external_exec_list
from .curdir_file import curdir_files


class CompletionType(Enum):
    CommandCompletion = 0
    FileCompletion = 1


def compute_matches(
    matches: list[str], text: str, completion_type: CompletionType
) -> list[str]:

    completion_list = []
    if completion_type == CompletionType.CommandCompletion:
        completion_list = list(builtin_commands) + external_exec_list
    else:
        completion_list = curdir_files

    matches = sorted(
        [txt + " " for txt in completion_list if txt.startswith(text) and txt != text]
    )

    if len(matches) == 0:
        matches.append(text)

    return matches


def outer_completer():
    matches = []
    prev_text = ""

    def completer(text: str, state: int) -> str | None:
        nonlocal matches
        nonlocal prev_text

        completion_type = CompletionType.CommandCompletion

        line_buffer = readline.get_line_buffer().split(" ")
        if line_buffer.__len__() > 1:
            completion_type = CompletionType.FileCompletion

        is_new_TAB = True if prev_text and prev_text != text else False

        try:
            if state == 0:
                if len(matches) > 0 and not is_new_TAB:
                    """
                    This is handling the second tab press. I have to manually print all the
                    values, otherwise the default string fortmatting won't pass codecrafters
                    tests



                    Why do it like this? 

                        Usually you wouldn't! You would just use the completeion display hook
                        from gnureadline. But macos sucks and don't support gnureadline. That's why I
                        am stuck with this kind of hacky solutions.

                    """

                    print()
                    match_string = " ".join(matches)
                    print(f"{match_string}")
                    print(f"$ {text}")

                    # Reset the nonlocal variables
                    matches = []
                    prev_text = ""

                    return None
                else:
                    prev_text = text
                    matches = compute_matches(matches, text, completion_type)

            if state > len(matches):
                return None

            return matches[state]
        except IndexError:
            return None

    return completer


# def outer_cwd_completer():
#     matches = []
#     prev_text = ""
#
#     def completer(text: str, state: int) -> str | None:
#         nonlocal matches
#         nonlocal prev_text
#
#         is_new_TAB = True if prev_text and prev_text != text else False
#
#         try:
#             if state == 0:
#                 if len(matches) > 0 and not is_new_TAB:
#                     """
#                     This is handling the second tab press. I have to manually print all the
#                     values, otherwise the default string fortmatting won't pass codecrafters
#                     tests
#
#
#
#                     Why do it like this?
#
#                         Usually you wouldn't! You would just use the completeion display hook
#                         from gnureadline. But macos sucks and don't support gnureadline. That's why I
#                         am stuck with this kind of hacky solutions.
#
#                     """
#
#                     print()
#                     match_string = " ".join(matches)
#                     print(f"{match_string}")
#                     print(f"$ {text}")
#
#                     # Reset the nonlocal variables
#                     matches = []
#                     prev_text = ""
#
#                     return None
#                 else:
#                     prev_text = text
#                     matches = compute_matches(matches, text)
#
#             if state > len(matches):
#                 return None
#
#             return matches[state]
#         except IndexError:
#             return None
#
#     return completer
