import pyxel

from entity import Entity, Rect
from states import FlyState, RunState


class Player(Entity):
    W = 12
    H = 16
    MAX_SPEED = 300

    def __init__(self):
        super().__init__(Rect(30, 35, Player.W, Player.H))
        self.state = FlyState(self)
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
            self.state = RunState(self)

        if pyxel.btn(pyxel.KEY_SPACE):
            self.v = -3
            if self.a == 0:
                self.a = 0.3
                self.state = FlyState(self)

        self.state.update()
