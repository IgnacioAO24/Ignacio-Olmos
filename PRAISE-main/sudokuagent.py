from environments import SimulatedSensor, SimulatedActuator
from agents import Agent
from statebuffer import StateBuffer
class BoardSensor(SimulatedSensor):

    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="board")
        return response["board"]
    

class PlaceNumberActuator(SimulatedActuator):

    def act(self, row: int, col: int, value: int):
        self._env.take_action(self._agent.id, "place", {"row": row, "col": col, "value": value})


class ClearCellActuator(SimulatedActuator):

    def act(self, row: int, col: int):
        self._env.take_action(self._agent.id, "clear", {"row": row, "col": col})

class SudokuAgent(Agent):
    SIZE = 9
    BOX = 3

    def __init__(self, env):
        super().__init__()
        env.add(self.id)
        placer = PlaceNumberActuator(env)
        placer.agent = self
        self.add_actuator("placer", placer)

        clearer = ClearCellActuator(env)
        clearer.agent = self
        self.add_actuator("clearer", clearer)

        board_sensor = BoardSensor(env)
        board_sensor.agent = self
        self.add_sensor("board_sensor", board_sensor)
        self._empty_cells = None
        self._pointer = 0
        self._finished = False
        self._env = env
    
    
        
    @property
    def finished(self):
        return self._finished
    
    def _find_empty_cells(self, board):
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if board[r][c] == 0]
    
    def _is_valid(self, board, row, col, value):
        for c in range(self.SIZE):
            if c != col and board[row][c] == value:
                return False

        for r in range(self.SIZE):
            if r != row and board[r][col] == value:
                return False

        box_row = self.BOX * (row // self.BOX)
        box_col = self.BOX * (col // self.BOX)
        for r in range(box_row, box_row + self.BOX):
            for c in range(box_col, box_col + self.BOX):
                if (r, c) != (row, col) and board[r][c] == value:
                    return False

        return True
    
    def function(self, percept):
        board = percept["board_sensor"]

        if self._empty_cells is None:
            self._empty_cells = self._find_empty_cells(board)

        if self._pointer >= len(self._empty_cells):
            self._finished = True
            print("Solved!")
            return {"name": "noop"}

        row, col = self._empty_cells[self._pointer]
        current_value = board[row][col]

        candidate = None
        for value in range(current_value + 1, 10):
            if self._is_valid(board, row, col, value):
                candidate = value
                break

        if candidate is not None:
            self._pointer += 1
            return {"name": "place", "params": {"row": row, "col": col, "value": candidate}}
        else:
            self._pointer -= 1
            if self._pointer < 0:
                self._finished = True
                print("No solution found.")
                return {"name": "noop"}
            return {"name": "clear", "params": {"row": row, "col": col}}

    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)

        action_actuators = {
            "place": (self._actuators["placer"], ["row", "col", "value"]),
            "clear": (self._actuators["clearer"], ["row", "col"]),
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(p) for p in expected_params]
            actuator.act(*args)

    def behave(self):
        percept = self._perceive()
        self._act(percept)
        
    def run(self, renderer = None):
        statebuffer = StateBuffer(self.id, self._env)
        renderer.observe(statebuffer)
        renderer.render(force=True, titulo="Tablero inicial")
        while not self.finished:
            self.behave()
            renderer.render()
        renderer.render(force=True, titulo="Tablero final")