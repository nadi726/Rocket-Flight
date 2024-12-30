import pyxel
from states import FlyState, RunState


class Player:
    W = 12
    H = 16
    MAX_SPEED = 300

    def __init__(self):
        self.x = 30
        self.y = 35
        self.v = 0.2
        self.a = 0.3

        self.state = FlyState()

    def update(self):
        self.v += min(self.a, self.MAX_SPEED)
        self.y += self.v

        if pyxel.btn(pyxel.KEY_SPACE):
            self.v = -3
        self.state.update()

    def draw(self):
        self.state.draw(self.x, self.y)