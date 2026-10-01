from typing import List, Tuple, Dict
from boards import SudokuRepository

def get_candidates(board):
    candidates = {}
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                posibles = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                using_row = set(board[row]) 
                using_col = set(board[i][col] for i in range(9))
                box_row = (row // 3)*3
                box_col = (col // 3) * 3
                using_box = set(board[r][c] for r in range(box_row, box_row +3) for c in range(box_col, box_col +3))
                candidates[(row, col)] = posibles - using_row - using_col - using_box
    return candidates

if __name__ == "__main__":
    repository = SudokuRepository()
    board = repository.load_board("easy/board01.json")
    candidates = get_candidates(board.grid)
    print(candidates)