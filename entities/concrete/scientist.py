from typing import Literal

import pyxel

from core.consts import TILE_SIZE
from core.frame_manager import Frame, FrameManager
from entities.entity import Entity, Rect

SCIENTIST_W = 9
SCIENTIST_H = 14


class Scientist(Entity):
    W = SCIENTIST_W
    H = SCIENTIST_H
    SPEED = 1
    FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE * 2, SCIENTIST_W, SCIENTIST_H) for i in range(6))
    REVERSED_FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE * 2, -SCIENTIST_W, SCIENTIST_H) for i in range(6))

    def __init__(self, direction: Literal[1, -1] = 1):
        super().__init__(Rect(pyxel.width, pyxel.height * 4 / 5 - self.H + 3, self.W, self.H))
        if direction == 1:
            self.frame_manager = FrameManager(self.FRAMES)
            self.vx = self.SPEED
        else:
            self.frame_manager = FrameManager(self.REVERSED_FRAMES)
            self.vx = -self.SPEED
