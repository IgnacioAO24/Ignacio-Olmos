import os
from SudokuWorld import SudokuEnvironment
from sudokuagent import SudokuAgent
from boards import SudokuRepository

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
    N = 45
    clear_terminal()
    difficulty = chosen_difficulty()
    print(repr(difficulty))
    repository = SudokuRepository()
    board_path = repository.random_path(difficulty)
    env = SudokuEnvironment(board_path)
    agent = SudokuAgent(env)

    print("Tablero inicial:")
    env.print_board()
    cont = 0
    while not agent.finished:
        cont += 1
        agent.behave()
        if cont % N == 0: 
            print("\nTablero actual:")
            env.print_board()
            
    print("\nTablero final:")
    env.print_board()