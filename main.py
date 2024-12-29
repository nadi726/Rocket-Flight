import pyxel

class App:
    def __init__(self):
        pyxel.init(320, 192)
        pyxel.load('./res.pyxres')
        pyxel.run(self.update, self.draw)
    
    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(30, 0, 0, 16, 0, 16, 16, 3)

App()