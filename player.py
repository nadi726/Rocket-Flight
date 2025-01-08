import pyxel

from entity import Entity, Rect
from frame_manager import Frame, FrameManager


class Player(Entity):
    W = 12
    H = 16
    MAX_SPEED = 300
    FLY_FRAMES = tuple(Frame(0, 16 * i, 0, 16, 16, 3) for i in range(1, 5))
    RUN_FRAMES = tuple(Frame(0, 16 * i, 16, 16, 16, 3) for i in range(7))

    def __init__(self):
        super().__init__(Rect(30, 35, Player.W, Player.H))
        self.frame = FrameManager(self.FLY_FRAMES)
        self.v = 0.2
        self.a = 0.3

    def update(self):
        super().update()
        self.v += min(self.a, self.MAX_SPEED)
        self.rect.y = max(0, self.rect.y + self.v)

        if self.rect.bottom >= pyxel.height * 4 / 5:
            self.rect.bottom = pyxel.height * 4 / 5 - 1
            self.v = 0
            self.a = 0
            self.frame = FrameManager(self.RUN_FRAMES)

        if pyxel.btn(pyxel.KEY_SPACE):
            self.v = -3
            if self.a == 0:
                self.a = 0.3
                self.frame = FrameManager(self.FLY_FRAMES)
