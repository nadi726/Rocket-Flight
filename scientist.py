from typing import Literal

import pyxel

from consts import TILE_SIZE
from entity import Entity, Rect
from frame_manager import Frame, FrameManager

SCIENTIST_W = 9
SCIENTIST_H = 14


class Scientist(Entity):
    W = SCIENTIST_W
    H = SCIENTIST_H
    FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE * 2, SCIENTIST_W, SCIENTIST_H) for i in range(6))
    REVERSED_FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE * 2, -SCIENTIST_W, SCIENTIST_H) for i in range(6))

    def __init__(self, direction: Literal[1, -1] = 1):
        super().__init__(Rect(pyxel.width, pyxel.height * 4 / 5 - self.H + 3, self.W, self.H))
        if direction == 1:
            self.frame_manager = FrameManager(self.FRAMES)
        else:
            self.frame_manager = FrameManager(self.REVERSED_FRAMES)
            self.vx = -1
