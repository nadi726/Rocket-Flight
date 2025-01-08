from typing import Literal

import pyxel

from entity import Entity, Rect
from frame_manager import Frame, FrameManager

W = 9
H = 14


class Scientist(Entity):
    W = W
    H = H
    FRAMES = tuple(Frame(0, 16 * i, 32, W, H, 3) for i in range(6))
    REVERSED_FRAMES = tuple(Frame(0, 16 * i, 32, -W, H, 3) for i in range(6))

    def __init__(self, direction: Literal[1, -1] = 1):
        super().__init__(Rect(pyxel.width, pyxel.height * 4 / 5 - self.H + 3, self.W, self.H))
        if direction == 1:
            self.frame = FrameManager(self.FRAMES)
            self.v = 0
        else:
            self.frame = FrameManager(self.REVERSED_FRAMES)
            self.v = -1

    def update(self):
        super().update()
        self.rect.x += self.v
