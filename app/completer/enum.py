from enum import Enum


class CompletionType(Enum):
    CommandCompletion = 0
    FileCompletion = 1
    NestedFileCompletion = 2
