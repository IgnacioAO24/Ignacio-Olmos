import json
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SudokuBoard:
    id: str
    difficulty: str
    grid: List[List[Optional[int]]]
    solution: Optional[List[List[int]]] = None

class SudokuRepository:
    def __init__(self, base_path:str = "board"):
        self._path = Path(base_path)
    def load_board(self, path:str) -> SudokuBoard:
        with open(self._path / path, "r") as f:
            data = json.load(f)
        return SudokuBoard(**data)
    def load_random(self, difficulty:str) -> SudokuBoard:
        files = list(self._path.glob(f"{difficulty}/*.json"))
        chosen = random.choice(files)
        return self.load_board(chosen.relative_to(self._path))
    def random_path(self, difficulty:str) -> str:
        files = list(self._path.glob(f"{difficulty}/*.json"))
        chosen = random.choice(files)
        return str(chosen.relative_to(self._path))        
if __name__ == "__main__":
    repo = SudokuRepository()
    board = repo.load_random()
   