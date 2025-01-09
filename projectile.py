import pyxel

import consts
from entity import Entity, Rect
from frame_manager import Frame, FrameManager

PROJECTILE_W = 15
PROJECTILE_H = 7
PROJECTILE_SPEED = 2.5

FRAMES = (Frame(0, 0, 6 * consts.TILE_SIZE, PROJECTILE_W, PROJECTILE_H),)


def make_projectile():
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - PROJECTILE_H)

    proj = Entity(Rect(consts.W, y, PROJECTILE_W, PROJECTILE_H))
    proj.frame_manager = FrameManager(FRAMES)
    proj.vx = -PROJECTILE_SPEED
    return proj
