from enum import Enum


class CompletionType(Enum):
    CommandCompletion = 0
    CurDirCompletion = 1
    NestedDirCompletion = 2
