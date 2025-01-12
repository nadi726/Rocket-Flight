import pyxel

import consts
from entity import Entity, Rect
from frame_manager import Frame, FrameManager

COIN_SIZE = 11
COIN_GAP = 3
START_X = consts.W
COIN_FRAMES = (Frame(0, consts.TILE_SIZE * 1, consts.TILE_SIZE * 6, COIN_SIZE, COIN_SIZE),)

SHAPE_SQUARE = """
****
****
****
****
"""

SHAPE_ARROW = """
__**
__***
___***
*******
********
*******
___***
__***
__**
"""

SHAPE_HORIZONTAL_LINE = """
***********
"""

SHAPE_ASCENDING_LINE = """
____*
___*
__*
_*
*
"""

SHAPE_DESCENDING_LINE = """
*
_*
__*
___*
____*
"""

SHAPES = (SHAPE_SQUARE, SHAPE_ARROW, SHAPE_HORIZONTAL_LINE, SHAPE_ASCENDING_LINE, SHAPE_DESCENDING_LINE)


def make_coins() -> set[Entity]:
    """Return a set of coins that form a shape from a random pool of shapes"""
    coins: set[Entity] = set()
    shape = SHAPES[pyxel.rndi(0, len(SHAPES) - 1)]

    rows = list(shape.split("\n"))
    full_height = COIN_SIZE * len(rows) + (len(rows) - 1) * COIN_GAP
    start_y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - full_height)

    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char == "*":
                x = START_X + j * (COIN_SIZE + COIN_GAP)
                y = start_y + i * (COIN_SIZE + COIN_GAP)
                coin_rect = Rect(x, y, COIN_SIZE, COIN_SIZE)
                coin = Entity(coin_rect)
                coin.frame_manager = FrameManager(COIN_FRAMES)
                coins.add(coin)

    return coins
