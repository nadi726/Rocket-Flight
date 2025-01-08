from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Literal

import pyxel

from frame_manager import FrameManager


@dataclass
class Rect:
    """
    Represents a rectangle with a position (x, y) and a size (w, h).

    Provides properties for the left, right, top and bottom sides of the rectangle.
    """

    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.left + self.w

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.top + self.h

    @left.setter
    def left(self, value: float):
        self.x = value

    @right.setter
    def right(self, value: float):
        self.left = value - self.w

    @top.setter
    def top(self, value: float):
        self.y = value

    @bottom.setter
    def bottom(self, value: float):
        self.top = value - self.h

    def __add__(self, other: "Rect"):
        return Rect(self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)

    def debug_draw(self, color: int = 3):
        pyxel.rect(self.x, self.y, self.w, self.h, color)


class HitBox:
    """
    Represents a collision box relative to an entity's position.

    Requires a reference to the entity before use.
    """

    NO_ENTITY_MSG = "HitBox must be associated with an Entity before use."

    def __init__(self, x: float, y: float, w: float, h: float):
        self.relative_x: float = x
        self.relative_y: float = y
        self._w: float = w
        self._h: float = h
        self.relative_rect = Rect(x, y, w, h)

    _entity: "Entity | None" = None

    @property
    def entity(self) -> "Entity":
        if self._entity is None:
            raise ValueError(self.NO_ENTITY_MSG)
        return self._entity

    @entity.setter
    def entity(self, value: "Entity"):
        self._entity = value

    def collides(self, other: "HitBox") -> bool:
        r1: Rect = self.abs_rect
        r2 = other.abs_rect
        return r1.left <= r2.right and r1.right >= r2.left and r1.top <= r2.bottom and r1.bottom >= r2.top

    @property
    def abs_rect(self):
        x = self.relative_rect.x + self.entity.rect.x
        y = self.relative_rect.y + self.entity.rect.y
        return Rect(x, y, self._w, self._h)

    def debug_draw(self, color: int = 9) -> None:
        r = self.abs_rect
        pyxel.rect(r.x, r.y, r.w, r.h, color)


@dataclass
class EntityPart:
    frame_manager: FrameManager = field(default_factory=FrameManager.empty)
    offset: tuple[float, float] = (0, 0)


class Entity:
    """
    A game entity with position, collision handling, and sprite management.

    An Entity can be either:
    1. A single-part entity:
        - The "parts" parameter is ignored.
        - After initialization, the "frame" property should be set manually.

    2. A multi-part entity:
        - Provide a sequence of parts.
        - Each part is a dictionary of the form:
          {"frame_manager": frame_manager, "offset": (x, y)}.
        - The "offset" key is optional.

    Both kinds of entities can have multiple hitboxes. If no hitbox is provided,
    the entity gets a default hitbox based on its dimensions.
    """

    def __init__(
        self,
        rect: Rect,
        parts: tuple[EntityPart, ...] | None = None,
        hitboxes: Iterable[HitBox] | None = None,
    ):
        self.rect = rect

        self.parts: tuple[EntityPart, ...] = parts or (EntityPart(),)

        self.hitboxes = hitboxes or [HitBox(0, 0, self.rect.w, self.rect.h)]
        for hitbox in self.hitboxes:
            hitbox.entity = self

    @property
    def frame(self) -> FrameManager:
        """Convenience property to access the main part's frame manager."""
        return self.parts[0].frame_manager

    @frame.setter
    def frame(self, value: FrameManager):
        """Convenience property to set the main part's frame manager."""
        self.parts[0].frame_manager = value

    def collides(self, other: "Entity") -> bool:
        return any(
            self_hitbox.collides(other_hitbox) for self_hitbox in self.hitboxes for other_hitbox in other.hitboxes
        )

    def update(self):
        # Extract unique FrameManager instances from parts
        unique_frame_managers = {part.frame_manager for part in self.parts}
        # Ensure the frames stay in sync by only updating unique frame managers
        for frame_manager in unique_frame_managers:
            frame_manager.update()

    def move(self, dx: float, dy: float):
        """Move the entity and update hitbox positions."""
        # Move the entity
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, *, debug: Literal["bounding box", "hitboxes", "all"] | None = "hitboxes"):
        """
        Draw the entity on the screen.

        Args:
            debug: Optional debug mode. Can be one of:
                - "bounding box": Draw the entity's bounding box.
                - "hitboxes": Draw the entity's hitboxes.
                - "all": Draw both the bounding box and hitboxes.
                - None: Don't draw any debug information (default).

        """
        if debug in ("bounding box", "all"):
            self.rect.debug_draw(color=3)
        if debug in ("hitboxes", "all"):
            for hitbox in self.hitboxes:
                hitbox.debug_draw()

        for part in self.parts:
            offset_x, offset_y = part.offset
            part.frame_manager.draw(self.rect.x + offset_x, self.rect.y + offset_y)
