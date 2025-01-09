import pyxel

import consts
from entity import Entity
from lasers import make_laser
from player import Player
from projectile import make_projectile
from scientist import Scientist


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.load("./res.pyxres")

        self.player = Player()
        self.scientists: set[Scientist] = {Scientist()}
        self.scrollables: set[Entity] = {*self.scientists}

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        for entity in self.scrollables:
            entity.update()

        self.scroll_entities()
        self.generate_entities()

    # Move all scrollables to the left, removing those that are past the screen
    def scroll_entities(self):
        to_remove: set[Entity] = set()
        for entity in self.scrollables:
            entity.rect.x -= 3
            if entity.rect.right < 0:
                to_remove.add(entity)
        self.scrollables -= to_remove

    # generate new entities for this frame
    def generate_entities(self):
        self.scrollables.update(self.generate_scientists() | self.generate_lasers() | self.generate_projectiles())

    def generate_scientists(self) -> set[Entity]:
        if pyxel.frame_count % 5 != 0 or pyxel.rndi(1, 10) != 1:
            return set()  # don't generate anything

        scientist = Scientist(direction=-1) if pyxel.rndi(1, 5) == 1 else Scientist()
        self.scientists.add(scientist)
        return {scientist}

    def generate_lasers(self) -> set[Entity]:
        if pyxel.frame_count % 100 == 0:
            return make_laser()
        return set()

    def generate_projectiles(self) -> set[Entity]:
        if pyxel.frame_count % pyxel.rndi(200, 204) == 0:
            return {
                make_projectile(),
            }
        return set()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, consts.W, consts.H)

        for entity in self.scrollables:
            entity.draw()
        self.player.draw()


App()
