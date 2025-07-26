
class Action:

    # Is there a static var inside a class in Python?
    VISUAL_REPRESENTATIONS = { 0: "↑", 1: "→", 2: "↓", 3: "←" }

    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y

    def __repr__(self) -> str:
        if self.x == 0 and self.y == 1:
            return self.VISUAL_REPRESENTATIONS[0] 
        if self.x == 1 and self.y == 0:
            return self.VISUAL_REPRESENTATIONS[1]
        if self.x == 0 and self.y == -1:
            return self.VISUAL_REPRESENTATIONS[2]
        if self.x == -1 and self.y == 0:
            return self.VISUAL_REPRESENTATIONS[3]
        
        raise Exception("Invalid move")