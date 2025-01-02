import pyxel

from entity import Entity
from frame_manager import FrameManager

W = 9
H = 14
class Scientist(Entity):
    W = W
    H = H
    FRAMES = tuple(((0, 16 * i, 32, W, H, 3) for i in range(6)))
    REVERSED_FRAMES = tuple(((0, 16 * i, 32, -W, H, 3) for i in range(6)))

    def __init__(self, direction = 1):
        if direction == 1:
            frame = self.FRAMES
            self.v = 0
        else:
            frame = self.REVERSED_FRAMES
            self.v = -1
        
        super().__init__(pyxel.width, pyxel.height * 4 / 5 - self.H + 3, self.W, self.H, frame)

    def update(self):
        self.x += self.v
        self.frame.update()