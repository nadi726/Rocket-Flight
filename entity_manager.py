import pyxel

import consts
from entity import Entity
from lasers import make_laser
from projectile import make_projectile
from scientist import Scientist

all_entities: set[Entity] = set()
scrollables: set[Entity] = set()
scientists: set[Entity] = set()
hazards: set[Entity] = set()
coins: set[Entity] = set()
player_bullets: set[Entity] = set()


def _generate_scientists() -> set[Entity]:
    if pyxel.frame_count % 5 != 0 or pyxel.rndi(1, 10) != 1:
        return set()  # don't generate anything

    scientist = Scientist(direction=-1) if pyxel.rndi(1, 5) == 1 else Scientist()
    scientists.add(scientist)
    return {scientist}

def _generate_lasers() -> set[Entity]:
    if pyxel.frame_count % 100 == 0:
        return make_laser()
    return set()

def _generate_projectiles() -> set[Entity]:
    if pyxel.frame_count % pyxel.rndi(200, 204) == 0:
        return {
            make_projectile(),
        }
    return set()

def _generate_coins() -> set[Entity]:
    return set()


# generate new entities for this frame
def _generate_entities():
    new_scientists = _generate_scientists()
    new_hazards = _generate_lasers() | _generate_projectiles()
    new_coins = _generate_coins()

    scientists.update(new_scientists)
    hazards.update(new_hazards)
    coins.update(new_coins)

    new_entities = new_scientists | new_hazards | new_coins
    scrollables.update(new_entities)
    all_entities.update(new_entities)


def _remove_entities():
    to_remove: set[Entity] = set()
    for entity in scrollables:
        if entity.rect.right < 0:
            to_remove.add(entity)

    to_remove.update([bullet for bullet in player_bullets if bullet.rect.top > consts.H])

    scrollables.difference_update(to_remove)
    to_remove -= scrollables
    scientists.difference_update(to_remove)
    to_remove -= scientists
    player_bullets.difference_update(to_remove)


def draw():
    for entity in scrollables:
        entity.draw()

def update():
    _remove_entities()
    _generate_entities()
    for entity in all_entities:
        entity.update()
        if entity in scrollables:
            entity.move(-3, 0)

