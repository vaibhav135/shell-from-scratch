from enum import Enum


class CompletionType(Enum):
    CommandCompletion = 0
    FileCompletion = 1
    NestedFileCompletion = 2
    DirectoryCompletion = 3
    BothDirAndFileCompletion = 4


class CommandType(Enum):
    FileType = ["cat", "less", "head", "tail", "wc", "grep"]
    DirType = ["cd", "rmdir"]
    BothFileAndDir = ["ls", "cp", "mv", "rm", "du", "chmod", "stat"]

    @classmethod
    def get_command_type(cls, command: str):
        for ct in cls:
            if command in ct.value:
                return ct.name
