import pyxel

from src.core import consts
from src.core.frame_manager import Frame, FrameManager
from src.entities.entity import Entity, Rect

BULLET_W = 3
BULLET_H = 4
BULLET_VY_RANGE = (3, 4)
BULLET_VX_RANGE = (-0.5, 0.4)
MAX_BULLETS = 3

FRAMES = (Frame(0, 2 * consts.TILE_SIZE, 6 * consts.TILE_SIZE, BULLET_W, BULLET_H),)


def _make_bullet(player_rect: Rect):
    x = pyxel.rndf(player_rect.left, player_rect.left + player_rect.w / 2 - BULLET_W)

    bullet = Entity(Rect(x, player_rect.bottom, BULLET_W, BULLET_H))
    bullet.frame_manager = FrameManager(FRAMES)
    bullet.vy = pyxel.rndf(*BULLET_VY_RANGE)
    bullet.vx = pyxel.rndf(*BULLET_VX_RANGE)
    return bullet


def make_player_bullets(player_rect: Rect):
    times = pyxel.rndi(1, 3)
    return {_make_bullet(player_rect) for _ in range(times)}
