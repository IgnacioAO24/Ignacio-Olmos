import os
from SudokuWorld import SudokuEnvironment
from sudokuagent import SudokuAgent
from boards import SudokuRepository
from sudokurenderers import ConsoleRenderer
from statebuffer import StateBuffer

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

def run(agent, env, renderer):
    statebuffer = StateBuffer(agent.id, env)
    renderer.observe(statebuffer)
    renderer.render(force=True, titulo="Tablero inicial")
    while not agent.finished:
        agent.behave()
        renderer.render()
    renderer.render(force=True, titulo="Tablero final")
    
if __name__ == '__main__':
    clear_terminal()
    print("Sudoku Solver")
    difficulty = chosen_difficulty()
    repository = SudokuRepository()
    board = repository.load_random(difficulty)
    env = SudokuEnvironment(board)
    agent = SudokuAgent(env)
    renderer = ConsoleRenderer()
    run(agent, env, renderer)
    
    
    
    
    #print(repr(difficulty))
    #print(board_path)