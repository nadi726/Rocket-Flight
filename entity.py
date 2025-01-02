from typing import Iterable
import pyxel
from frame_manager import FrameManager, Frame
from dataclasses import dataclass


class RectMixin:
    """A mixin providing convenient properties for rectangle-like objects.

    Requires the object to have attributes: x, y, w, h.
    """

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

@dataclass
class HitBox(RectMixin):
    """Represents a collision box relative to an entity's position.

    Requires a reference to the entity before use.
    """
    relative_x : float # relative to entity x
    relative_y : float # relative to entity y
    w : float
    h : float
    entity: "Entity" = None  # Must asign entity before using a HitBox
    
    @property
    def x(self):
        self.ensure_entity()
        return self.entity.x + self.relative_x
    
    @property
    def y(self):
        self.ensure_entity()
        return self.entity.y + self.relative_y
    
    def collides(self, other : "HitBox"):
        self.ensure_entity()
        return self.left <= other.right and self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top
    
    def ensure_entity(self):
        if self.entity is None:
            raise ValueError("HitBox must be associated with an Entity.")
        
    def debug_draw(self, color=9):
        pyxel.rect(self.x, self.y, self.w, self.h, color)


class Entity(RectMixin):
    """A game entity with position, collision handling, and sprite management."""

    def __init__(self, x : float, y : float, w : float, h : float, frame : Iterable[Frame] = (Frame.empty(),), hitboxes : list[HitBox] = None):
        self.x : float = x
        self.y : float = y
        self.w : int = w
        self.h : int = h
        self.frame = FrameManager(frame)

        self.hitboxes = hitboxes
        if hitboxes is None:
            self.hitboxes = [HitBox(0, 0, w, h)]
        for hitbox in self.hitboxes:
            hitbox.entity = self

    def collides(self, other):
        return any(
            self_hitbox.collides(other_hitbox)
            for self_hitbox in self.hitboxes
            for other_hitbox in other.hitboxes
        )
    
    def update(self):
        self.frame.update()
    
    def draw(self, show_bounding_box=False ,show_hitboxes=False):
        if show_bounding_box:
            pyxel.rect(self.x, self.y, self.w, self.h, 3)
        if show_hitboxes:
            for hitbox in self.hitboxes:
                hitbox.debug_draw()
        self.frame.draw(self.x, self.y)
