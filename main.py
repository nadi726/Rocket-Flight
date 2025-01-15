import pyxel

import consts
from entity_manager import EntityManager
from player import Player


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.load("./res.pyxres")

        self.entity_manager = EntityManager()
        self.player = Player(self.entity_manager)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.player.on_fly()

        self.entity_manager.update()
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, consts.W, consts.H)

        self.entity_manager.draw()
        self.player.draw()


App()
