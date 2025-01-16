from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING

import pyxel

from core import consts
from entities.concrete import (
    Scientist,
    make_coins,
    make_laser,
    make_player_bullets,
    make_projectile,
)
from entities.entity import Entity

if TYPE_CHECKING:
    from entities.entity import Rect


SCROLLABLE = "scrollable"
SCIENTIST = "scientist"
HAZARD = "hazard"
COIN = "coin"
PLAYER_BULLET = "player_bullet"

TAGS = (SCROLLABLE, SCIENTIST, HAZARD, COIN, PLAYER_BULLET)


class EntityCollection:
    def __init__(self):
        self.entities: set[Entity] = set()
        self.groups: dict[str, set[Entity]] = {}
        for tag in TAGS:
            self.groups[tag] = set()

    def __iter__(self):
        return iter(self.entities)

    def add(self, entity: Entity, tags: Iterable[str] = ()):
        self.entities.add(entity)
        for tag in tags:
            self.groups[tag].add(entity)

    def add_batch(self, entities: Iterable[Entity], tags: Iterable[str] = ()):
        self.entities.update(entities)
        for tag in tags:
            self.groups[tag].update(entities)

    def remove(self, entity: Entity):
        self.entities.discard(entity)
        for tag_group in self.groups.values():
            tag_group.discard(entity)

    def remove_batch(self, entities: Iterable[Entity]):
        self.entities.difference_update(entities)
        for tag_group in self.groups.values():
            tag_group.difference_update(entities)

    def get(self, tag: str) -> set[Entity]:
        return self.groups[tag]


class EntityManager:
    PROJECTILE_SPAWN_CHANCE = 40
    COINS_SPAWN_CHANCE = 30

    def __init__(self):
        self.entities = EntityCollection()
        self.generator = self._entity_generator()

    def _entity_generator(self) -> Generator[tuple[set[Entity], tuple[str, ...]]]:
        while True:
            yield (make_laser(), (SCROLLABLE, HAZARD))
            if pyxel.rndf(1, 100) < self.PROJECTILE_SPAWN_CHANCE:
                yield ({make_projectile()}, (SCROLLABLE, HAZARD))
            if pyxel.rndf(1, 100) < self.COINS_SPAWN_CHANCE:
                yield (make_coins(), (SCROLLABLE, COIN))

    def _generate_entities(self):
        if pyxel.frame_count % 40 != 0:
            return
        self.entities.add_batch(*next(self.generator))

    def _generate_scientists(self):
        if pyxel.frame_count % 5 != 0 or pyxel.rndi(1, 10) != 1:
            return
        scientist = Scientist(direction=-1) if pyxel.rndi(1, 5) == 1 else Scientist()
        self.entities.add(scientist, (SCROLLABLE, SCIENTIST))

    def _remove_entities(self):
        to_remove = {e for e in self.entities.get(SCROLLABLE) if e.rect.right < 0}
        to_remove.update([b for b in self.entities.get(PLAYER_BULLET) if b.rect.top > consts.H])
        self.entities.remove_batch(to_remove)

    def _move_scrollables(self):
        for entity in self.entities.get(SCROLLABLE):
            entity.move(-consts.SCROLL_SPEED, 0)

    def make_player_bullets(self, player_rect: "Rect"):
        new_bullets = make_player_bullets(player_rect)
        self.entities.add_batch(new_bullets, (PLAYER_BULLET,))

    def update(self):
        self._generate_entities()
        self._generate_scientists()
        self._remove_entities()
        self._move_scrollables()

        for entity in self.entities:
            entity.update()

    def draw(self):
        for entity in self.entities:
            entity.draw()
