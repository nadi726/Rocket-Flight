import pyxel

from core import consts
from core.background import Background
from core.entity_manager import EntityManager
from entities.concrete.player import Player


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.load("../resources/res.pyxres")

        self.entity_manager = EntityManager()
        self.player = Player(self.entity_manager)
        self.background = Background()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.player.on_fly()

        self.background.update()
        self.entity_manager.update()
        self.player.update()

    def draw(self):
        self.background.draw()
        self.entity_manager.draw()
        self.player.draw()
