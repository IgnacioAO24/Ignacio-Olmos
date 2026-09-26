from environments import SimulatedEnvironment
from boards import SudokuRepository
class SudokuEnvironment(SimulatedEnvironment):
    def __init__(self, board_path: str):
        self.repo = SudokuRepository()
        super(SudokuEnvironment, self).__init__()
        board = self.repo.load_board(board_path)
        self.board = [row[:] for row in board.grid]

    def print_board(self):
        for row in self.board:
            print(" ".join(str(v) if v != 0 else '.' for v in row))
            
    def get_property (self, agent_id: int, property_name: str) -> dict:
        if agent_id in self._agents:
            response = {"agent": agent_id}
            if property_name == "board":
                response["board"] = [row[:] for row in self.board]
            else:
                print(f"invalid property: {property_name}")
            return response
        return {}
    

    def take_action (self, agent_id:int, action_name:str, params:dict = {}) -> None:
        if agent_id in self._agents:
            if action_name == "place":
                row, col, value = params.get("row"), params.get("col"), params.get("value")
                self.board[row][col] = value
            elif action_name == "clear":
                    row, col = params.get("row"), params.get("col")
                    self.board[row][col] = 0
            else: 
                    print (f"invalid action: {action_name}")