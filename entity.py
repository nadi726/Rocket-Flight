import pyxel
from frame_manager import FrameManager

class Entity:
    def __init__(self, x : float, y : float, w : int, h : int, frame = ((0, 0, 0, 0, 0, 0))):
        self.x : float = x
        self.y : float = y
        self.w : int = w
        self.h : int = h
        self.frame = FrameManager(frame)
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self):
        return self.left + self.w
    
    @property
    def top(self):
        return self.y

    @property
    def bottom(self) -> float:
        return self.top + self.h
    
    @left.setter
    def left(self, value):
        self.x = value

    @right.setter
    def right(self, value):
        self.left = value - self.w

    @top.setter
    def top(self, value):
        self.y = value

    @bottom.setter
    def bottom(self, value):
        self.top = value - self.h

    def collides(self, other):
        return self.left <= other.right and self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top
    
    def update(self):
        self.frame.update()
    
    def draw(self, show_bounding_box=False):
        if show_bounding_box:
            pyxel.rect(self.x, self.y, self.w, self.h, 3)
        self.frame.draw(self.x, self.y)