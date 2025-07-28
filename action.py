
from state import State


class Action:

    # Is there a static var inside a class in Python?
    VISUAL_REPRESENTATIONS = { 0: "↑", 1: "→", 2: "↓", 3: "←" }

    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y

    def __str__(self) -> str:
        if self.x == 0 and self.y == 1:
            return self.VISUAL_REPRESENTATIONS[0] 
        if self.x == 1 and self.y == 0:
            return self.VISUAL_REPRESENTATIONS[1]
        if self.x == 0 and self.y == -1:
            return self.VISUAL_REPRESENTATIONS[2]
        if self.x == -1 and self.y == 0:
            return self.VISUAL_REPRESENTATIONS[3]
        
        print(f"self.x: {self.x}")
        print(f"self.y: {self.y}")
        raise Exception("Invalid action")
    
    def __add__(self, other):
        return State(other.x + self.x,  other.y + self.y)