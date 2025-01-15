from collections.abc import Generator
from enum import Enum
from typing import TYPE_CHECKING

import pyxel

import consts
from coins import make_coins
from entity import Entity
from lasers import make_laser
from player_bullets import make_player_bullets
from projectile import make_projectile
from scientist import Scientist

if TYPE_CHECKING:
    from entity import Rect


class EntityType(Enum):
    SCIENTIST = 0
    LASER = 1
    PROJECTILE = 2
    COIN = 3
    PLAYER_BULLET = 4


class EntityManager:
    PROJECTILE_SPAWN_CHANCE = 40
    COINS_SPAWN_CHANCE = 30

    def __init__(self):
        self.all_entities: set[Entity] = set()
        self.scrollables: set[Entity] = set()
        self.scientists: set[Entity] = set()
        self.hazards: set[Entity] = set()
        self.coins: set[Entity] = set()
        self.player_bullets: set[Entity] = set()
        self.generator = self._entity_generator()

    def _generate_scientists(self):
        if pyxel.frame_count % 5 != 0 or pyxel.rndi(1, 10) != 1:
            return
        scientist = Scientist(direction=-1) if pyxel.rndi(1, 5) == 1 else Scientist()
        self.scientists.add(scientist)
        self.all_entities.add(scientist)
        self.scrollables.add(scientist)

    def _remove_entities(self):
        to_remove = {e for e in self.scrollables if e.rect.right < 0}
        to_remove.update([b for b in self.player_bullets if b.rect.top > consts.H])

        self.scrollables -= to_remove
        self.scientists -= to_remove
        self.player_bullets -= to_remove
        self.all_entities -= to_remove

    def _entity_generator(self) -> Generator[tuple[set[Entity], EntityType], None, None]:
        while True:
            yield (make_laser(), EntityType.LASER)
            if pyxel.rndf(1, 100) < self.PROJECTILE_SPAWN_CHANCE:
                yield ({make_projectile()}, EntityType.PROJECTILE)
            if pyxel.rndf(1, 100) < self.COINS_SPAWN_CHANCE:
                yield (make_coins(), EntityType.COIN)

    def _generate_entities(self):
        if pyxel.frame_count % 40 != 0:
            return
        entities, entity_type = next(self.generator)
        self.all_entities.update(entities)
        self.scrollables.update(entities)
        match entity_type:
            case EntityType.LASER | EntityType.PROJECTILE:
                self.hazards.update(entities)
            case EntityType.COIN:
                self.coins.update(entities)
            case _:
                pass

    def make_player_bullets(self, player_rect: "Rect"):
        new_bullets = make_player_bullets(player_rect)
        self.player_bullets.update(new_bullets)
        self.all_entities.update(new_bullets)

    def update(self):
        self._generate_entities()
        self._generate_scientists()
        self._remove_entities()

        for entity in self.all_entities:
            entity.update()
            if entity in self.scrollables:
                entity.move(-consts.SCROLL_SPEED, 0)

    def draw(self):
        for entity in self.all_entities:
            entity.draw()

