import os


def has_backslash(char: str) -> bool:
    if char == r"\ "[0]:
        return True

    return False


def path_exists(path: str) -> bool:
    if os.access(path, os.X_OK):
        return True
    return False


def in_path(command: str, paths: list[str]) -> tuple[str, bool]:
    for path in paths:
        fullpath = os.path.join(path, command)
        if path_exists(fullpath):
            return fullpath, True

    return "", False
