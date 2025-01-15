from typing import TYPE_CHECKING

import pyxel

from consts import FLOOR_Y, TILE_SIZE
from entity import Entity, Rect
from frame_manager import Frame, FrameManager

if TYPE_CHECKING:
    from entity_manager import EntityManager


class Player(Entity):
    START_X, START_Y = 30, 35
    W = 12
    H = 16
    MAX_SPEED = 300
    FLY_FRAMES = tuple(Frame(0, TILE_SIZE * i, 0, TILE_SIZE, TILE_SIZE) for i in range(1, 5))
    RUN_FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE, TILE_SIZE, TILE_SIZE) for i in range(7))

    def __init__(self, entity_manager: "EntityManager"):
        super().__init__(Rect(self.START_X, self.START_Y, Player.W, Player.H))
        self.frame_manager = FrameManager(self.FLY_FRAMES)
        self.vy = 0.2
        self.a = 0.3
        self.entity_manager = entity_manager

    def update(self):
        super().update()
        self.vy += min(self.a, self.MAX_SPEED)
        self.rect.y = max(0, self.rect.y)

        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y - 1
            self.vy = 0
            self.a = 0
            self.frame_manager = FrameManager(self.RUN_FRAMES)

    def on_fly(self):
        self.vy = -3
        if self.a == 0:
            self.a = 0.3
            self.frame_manager = FrameManager(self.FLY_FRAMES)
        if pyxel.frame_count % 3 == 0:
            self.entity_manager.make_player_bullets(self.rect)
