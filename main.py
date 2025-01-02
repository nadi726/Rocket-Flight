import pyxel
from entity import Entity
from player import Player
from scientist import Scientist
from lasers import make_laser

class App:
    def __init__(self):
        pyxel.init(320, 192)
        pyxel.load('./res.pyxres')

        self.player = Player()
        self.scientists : set[Scientist] = {Scientist()}
        self.scrollables : set[Entity] = {*self.scientists}

        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()
        for entity in self.scrollables:
            entity.update()

        self.scroll_entities()
        self.generate_entities()

    # Move all scrollables to the left, removing those that are past the screen
    def scroll_entities(self):
        to_remove = set()
        for entity in self.scrollables:
            entity.x -= 3
            if entity.right < 0:
                to_remove.add(entity)
        self.scrollables -= to_remove
    
    # generate new entities for this frame
    def generate_entities(self):
        self.scrollables.update(self.generate_scientists() | self.generate_lasers())
    
    def generate_scientists(self):
        if pyxel.frame_count % 5 != 0 or pyxel.rndi(1, 10) != 1:
            return set() # don't generate anything
        
        if pyxel.rndi(1, 5) == 1:
            scientist = Scientist(direction=-1)
        else:
            scientist = Scientist()
        self.scientists.add(scientist)
        return {scientist}
    
    def generate_lasers(self):
        if pyxel.frame_count % 100 == 0:
            return make_laser()
        return set()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height)
        
        for entity in self.scrollables:
            entity.draw()
        self.player.draw()

App()