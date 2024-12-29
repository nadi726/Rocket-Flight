import pyxel
from frame_manager import FrameManager
class Player:
    W = 12
    H = 16
    FLY_FRAMES = [[0, 16 * i, 0, 16, 16, 3] for i in range(1, 5)]
    RUN_FRAMES = [[0, 16 *i, 16, 16, 16, 3] for i in range(7)]

    def __init__(self):
        self.x = 30
        self.y = 35
        self.frame = FrameManager(self.RUN_FRAMES)

    def update(self, dt):
        self.frame.update(dt)

    def draw(self):
        self.frame.draw(self.x, self.y)