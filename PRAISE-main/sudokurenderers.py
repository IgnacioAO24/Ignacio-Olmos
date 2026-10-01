from renderers import IRenderer

class ConsoleRenderer(IRenderer):
    def __init__(self):
        self.environment_statebuffer = {}
        self.cont = 0
        self.N = 25
    def observe(self, statebuffer):
        self.environment_statebuffer = statebuffer
    def render(self, force = False):
        state = self.environment_statebuffer.get_state()
        if state:
            self.cont += 1
            if self.cont % self.N == 0 or force:
                print("\nTablero actual:")
                for row in state["board"]:
                  print(" ".join(str(v) if v != 0 else '.' for v in row))
                  
