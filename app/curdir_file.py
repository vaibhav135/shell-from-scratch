from pathlib import Path


class CurDirFiles:
    def __init__(self):
        self.curdir = Path.cwd()
        self.curdir_files = []

        for file in self.curdir.iterdir():
            if file.is_file():
                self.curdir_files.append(file.name)

    def get_curdir_files(self):
        return self.curdir_files


curdir_files = CurDirFiles().get_curdir_files()
