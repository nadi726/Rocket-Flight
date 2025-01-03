import pyxel
import consts
from entity import Entity, HitBox
from frame_manager import Frame, FrameManager

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
    elif direction == 3:
        return make_diagonal1(x, size)
    
def make_horizontal(x, size):
    height = 16
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)

    left_frame = FrameManager(Frame(0, 16 + 8 * i, 48, 5, 16, 3) for i in range(4))
    middle_frame = FrameManager(Frame(0, 48 + 16 * i, 48, 16, 10, 3) for i in range(4))
    right_frame = FrameManager(Frame(0, 16 + 8 * i, 48, -5, 16, 3) for i in range(4))

    middle_parts = ({"frame_manager" : middle_frame, "offset" : (5 + m * 16, 3)} for m in range(size))
    parts = ({"frame_manager" : left_frame}, {"frame_manager" : right_frame, "offset" : (5 + size * 16, 0)}, *middle_parts)
    
    left_hitbox = HitBox(0, 0, 5, 16)
    middle_hitboxes = (HitBox(5 + 16 * m, 3, 16, 10) for m in range(size))
    right_hitbox = HitBox(5 + size * 16, 0, 5, 16)
    hitboxes = (left_hitbox, *middle_hitboxes, right_hitbox)
    
    laser = Entity(x, y, 5 * 2 + 16 * size, height, parts=parts, hitboxes=hitboxes)
    return {laser, }

def make_vertical(x, size):
    height = 5 * 2 + size * 16
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)

    top_frame = FrameManager(Frame(0, 16 * i, 64, 16, 5, 3) for i in range(4))
    middle_frame = FrameManager(Frame(0, 64 + 16 * i, 64, 10, 16, 3) for i in range(4))
    bottom_frame = FrameManager(Frame(0, 16 * i, 64, 16, -5, 3) for i in range(4))

    middle_parts = ({"frame_manager" : middle_frame, "offset" : (3, 5 + 16 * m)} for m in range(size))
    parts = ({"frame_manager" : top_frame}, *middle_parts, {"frame_manager" : bottom_frame, "offset" : (0, 5 + size * 16)})
    
    top_hitbox = HitBox(0, 0, 16, 5)
    middle_hitboxes = (HitBox(3, 5 + 16 * m, 10, 16) for m in range(size))
    bottom_hitbox = HitBox(0, 5 + size * 16, 16, 5)
    hitboxes = (top_hitbox, *middle_hitboxes, bottom_hitbox)
    
    laser = Entity(x, y, 16, height, parts=parts, hitboxes=hitboxes)
    return {laser, }

def make_diagonal1(x, size):
    height = 16 * (size + 2)
    y = pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)
    left_frame = tuple(Frame(0, 48 + 16 * i, 80, 16, 16, 3) for i in range(4))