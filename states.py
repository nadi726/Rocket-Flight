from frame_manager import FrameManager

class PlayerState:
    def draw(self, x, y):
        self.frame.draw(x, y)

class FlyState(PlayerState):
    FLY_FRAMES = [[0, 16 * i, 0, 16, 16, 3] for i in range(1, 5)]
    def __init__(self):
        self.frame = FrameManager(self.FLY_FRAMES)

    def update(self):
        self.frame.update()

class RunState(PlayerState):
    RUN_FRAMES = [[0, 16 *i, 16, 16, 16, 3] for i in range(7)]

    def __init__(self):
        self.frame = FrameManager(self.RUN_FRAMES)