import pyxel

import consts
from entity_manager import entity_manager
from player import Player


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.load("./res.pyxres")

        self.player = Player()

        pyxel.run(self.update, self.draw)

    def update(self):
        entity_manager.update()
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, consts.W, consts.H)

        entity_manager.draw()
        self.player.draw()


App()
