import time
import pyxel
from player import Player

class App:
    def __init__(self):
        pyxel.init(320, 192)
        pyxel.load('./res.pyxres')

        self.player = Player()

        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        self.player.draw()

App()