import time
import pyxel
from player import Player

class App:
    def __init__(self):
        pyxel.init(320, 192)
        pyxel.load('./res.pyxres')

        self.player = Player()

        self.dt = 0
        self.time = time.monotonic()

        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.update_dt()
        self.player.update(self.dt)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        self.player.draw()
    
    def update_dt(self):
        current_time = time.monotonic()
        self.dt = current_time - self.time
        self.time = current_time

App()