import os
from SudokuWorld import SudokuEnvironment
from sudokuagent import SudokuAgent
from boards import SudokuRepository
from sudokurenderers import ConsoleRenderer

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def chosen_difficulty():
    options = {"1": "easy", "2": "medium", "3": "hard"}
    mensaje = """choose a difficulty
    1) easy
    2) medium
    3) hard
    """
    difficulty = input(mensaje)
    return options [difficulty]
    
if __name__ == '__main__':
    print("Sudoku Solver")
    clear_terminal()
    difficulty = chosen_difficulty()
    print(repr(difficulty))
    repository = SudokuRepository()
    board_path = repository.random_path(difficulty)
    print(board_path)
    env = SudokuEnvironment(board_path)
    agent = SudokuAgent(env)
    renderer = ConsoleRenderer()
    agent.run(renderer)