import pyxel
import consts
from entity import Entity
from frame_manager import Frame

HORIZONTAL = 1
VERTICAL = 2
DIAGONAL1 = 3
DIAGONAL2 = 4

def make_laser(direction=1):
    size = pyxel.rndi(2, 5)
    x = pyxel.width
    if direction == 1:
        return make_horizontal(x, size)
    elif direction == 2:
        return make_vertical(x, size)
    
def make_horizontal(x, size):
    height = 16
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)
    left_frame = tuple((0, 16 + 8 * i, 48, 5, 16, 3) for i in range(4))
    middle_frame = tuple((0, 48 + 16 * i, 48, 16, 10, 3) for i in range(4))
    right_frame = tuple((0, 16 + 8 * i, 48, -5, 16, 3) for i in range(4))

    left = Entity(x, y, 5, 16, left_frame)
    middle_parts ={Entity(x + 5 + 16 * m, y + 3, 16, 10, middle_frame) for m in range(size)}
    right = Entity(x + 5 + size * 16, y, 5, 16, right_frame)

    return middle_parts | {left, right}

def make_vertical(x, size):
    height = 5 * 2 + size * 16
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)
    top_frame = tuple(Frame(0, 16 * i, 64, 16, 5, 3) for i in range(4))
    middle_frame = tuple(Frame(0, 64 + 16 * i, 64, 10, 16, 3) for i in range(4))
    bottom_frame = tuple(Frame(0, 16 * i, 64, 16, -5, 3) for i in range(4))

    top = Entity(x, y, 16, 5, top_frame)
    middle_parts ={Entity(x + 3, y + 5 + 16 * m, 10, 16, middle_frame) for m in range(size)}
    bottom = Entity(x, y + 5 + size * 16, 16, 5, bottom_frame)

    return middle_parts | {top, bottom}


