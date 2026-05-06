from pathlib import Path
from typing import List
from .constant import external_paths


class ExternalExecutables:
    def __init__(self):
        self.external_excutables = []
        for path in external_paths:
            path = Path(path)
            if Path.is_dir(path):
                for f in Path(path).iterdir():
                    self.external_excutables.append(f.name)

    def get_external_executables(self) -> List[str]:
        return self.external_excutables


external_exec_list = ExternalExecutables().get_external_executables()
