"""
Provides functions and constants for creating laser entities in various shapes and orientations,
including horizontal, vertical, and diagonal configurations. Each laser entity is composed of animated parts
with corresponding hitboxes for precise collision detection.

For external use, the `make_laser` function is the main entry point, enabling the generation of a random
laser entity with varying size and alignment.
"""

from collections.abc import Callable, Iterable

import pyxel

import consts
from consts import TILE_SIZE
from entity import Entity, EntityPart, HitBox, Rect
from frame_manager import Frame, FrameManager

# constants
FRAME_COUNT = 4  # Total of frames for each laser part
LASER_SIZE_BOUNDS = (3, 6)  # min size and max size for random laser generation

HALF_TILE = TILE_SIZE // 2
LASER_X = consts.W

# Horizontal
BASE_W = 5
BASE_H = TILE_SIZE
MIDDLE_W = 16
MIDDLE_H = 10
MIDDLE_Y_OFFSET = 3

# Diagonal
D_BASE_V = 5 * TILE_SIZE
D_PART_W = TILE_SIZE
D_PART_H = TILE_SIZE
D_HALF = D_PART_W // 2
D_BASE_HITBOX_OFFSET = 3


# diagonal helpers
def diag_middle_edge(size: int):
    """Return farthest edge of middle part - bottom & right"""
    return D_HALF * size


def diag_offset(size: int) -> tuple[int, int]:
    """Return offsets for diagonal's right x and bottom y."""
    edge = D_HALF * size + D_BASE_HITBOX_OFFSET + 1
    return edge, edge


# General helper functions
def make_frame_manager(  # noqa: PLR0913
    base_u: float,
    base_v: float,
    step_u: float,
    step_v: float,
    width: float,
    height: float,
    img: pyxel.Image | int = 0,
    colkey: int = 3,
    count: int = FRAME_COUNT,
    frame_delay: int = 2,
):
    """
    Create a FrameManager with a sequence of frames.

    All frames are generated from the given pyxel image, with the
    given base position and step sizes. The other parameters are
    forwarded to the FrameManager constructor.

        base_u, base_v: The x and y of the first frame in the image.
        step_u, step_v: The xand y steps between frames.
    """
    return FrameManager(
        tuple(Frame(img, base_u + step_u * i, base_v + step_v * i, width, height, colkey) for i in range(count)),
        frame_delay=frame_delay,
    )


def make_hitboxes(  # noqa: PLR0913
    base_x: float,
    base_y: float,
    step_x: float,
    step_y: float,
    width: float,
    height: float,
    count: int,
):
    """
    Generate hitboxes for laser parts.

        base_x, base_y: Start position.
        step_x, step_y: Per-hitbox offset.
        width, height: Dimensions of hitboxes.
        count: Number of hitboxes.
    """
    return [HitBox(base_x + step_x * i, base_y + step_y * i, width, height) for i in range(count)]


def make_parts(frame_managers: Iterable[FrameManager], offsets: Iterable[tuple[float, float]]):
    """
    Combine frame managers with their offsets into a sequence of parts.

        frame_managers: An iterable of FrameManager objects.
        offsets: An iterable of (x, y) tuples.

    Returns a generator of parts.
    """
    return tuple(
        EntityPart(frame_manager, offset) for frame_manager, offset in zip(frame_managers, offsets, strict=False)
    )


def generate_y(height: int):
    """Randomaly generate the laser's y, taking into account height"""
    return pyxel.rndi(consts.CEILING_Y, consts.FLOOR_Y - height)


def make_horizontal(size: int) -> set[Entity]:
    width = BASE_W * 2 + MIDDLE_W * size
    height = BASE_H
    y = generate_y(height)

    # Define frame managers for left, middle, and right parts
    left_frame = make_frame_manager(TILE_SIZE, TILE_SIZE * 3, HALF_TILE, 0, BASE_W, BASE_H)
    middle_frame = make_frame_manager(TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE, 0, MIDDLE_W, MIDDLE_H)
    right_frame = make_frame_manager(TILE_SIZE, TILE_SIZE * 3, HALF_TILE, 0, -BASE_W, BASE_H)

    # Create parts with frame managers and offsets
    parts = (EntityPart(left_frame),)
    parts += tuple(EntityPart(middle_frame, (BASE_W + m * MIDDLE_W, MIDDLE_Y_OFFSET)) for m in range(size))
    parts += (EntityPart(right_frame, (BASE_W + size * MIDDLE_W, 0)),)

    # Define hitboxes for each section
    hitboxes = [HitBox(0, 0, BASE_W, BASE_H)]
    hitboxes += make_hitboxes(BASE_W, MIDDLE_Y_OFFSET, MIDDLE_W, 0, MIDDLE_W, MIDDLE_H, size)
    hitboxes += [HitBox(BASE_W + size * MIDDLE_W, 0, BASE_W, BASE_H)]

    return {
        Entity(Rect(LASER_X, y, width, height), parts=parts, hitboxes=hitboxes),
    }


def make_vertical(size: int) -> set[Entity]:
    height = BASE_W * 2 + size * TILE_SIZE
    y = generate_y(height)

    # Define frame managers for left, middle, and right parts
    top_frame = make_frame_manager(0, TILE_SIZE * 4, TILE_SIZE, 0, BASE_H, BASE_W)
    middle_frame = make_frame_manager(TILE_SIZE * 4, TILE_SIZE * 4, TILE_SIZE, 0, MIDDLE_H, MIDDLE_W)
    bottom_frame = make_frame_manager(0, TILE_SIZE * 4, TILE_SIZE, 0, BASE_H, -BASE_W)

    # Create parts with frame managers and offsets
    parts = (EntityPart(top_frame),)
    parts += tuple(EntityPart(middle_frame, (MIDDLE_Y_OFFSET, BASE_W + m * MIDDLE_W)) for m in range(size))
    parts += (EntityPart(bottom_frame, (0, BASE_W + size * MIDDLE_W)),)

    # Define hitboxes for each section
    hitboxes = [HitBox(0, 0, BASE_H, BASE_W)]
    hitboxes += make_hitboxes(MIDDLE_Y_OFFSET, BASE_W, 0, MIDDLE_W, MIDDLE_H, MIDDLE_W, size)
    hitboxes += [(HitBox(0, BASE_W + size * MIDDLE_W, BASE_H, BASE_W))]

    return {
        Entity(Rect(LASER_X, y, BASE_H, height), parts=parts, hitboxes=hitboxes),
    }


def make_diagonal1(size: int) -> set[Entity]:
    """A single diagonal laser, top-left to bottom-right"""
    height = D_HALF * 2 + D_HALF * size
    y = generate_y(height)

    # Define frame managers for left, middle, and right parts
    left_frame = make_frame_manager(0, D_BASE_V, TILE_SIZE, 0, D_PART_W, D_PART_H)
    middle_frame = make_frame_manager(TILE_SIZE * 4, D_BASE_V, TILE_SIZE, 0, D_PART_W, D_PART_H)
    right_frame = make_frame_manager(0, D_BASE_V, TILE_SIZE, 0, -D_PART_W, -D_PART_H)

    # Create parts with frame managers and offsets
    parts = tuple(EntityPart(middle_frame, (D_HALF * m, D_HALF * m)) for m in range(1, size))
    parts += (EntityPart(left_frame),)
    parts += (EntityPart(right_frame, (diag_middle_edge(size), diag_middle_edge(size))),)

    # Define hitboxes for each section
    hitboxes = [HitBox(D_BASE_HITBOX_OFFSET, D_BASE_HITBOX_OFFSET, D_HALF + 1, D_HALF + 1)]
    hitboxes += make_hitboxes(D_HALF, D_HALF, D_HALF, D_HALF, D_HALF, D_HALF, size)
    hitboxes += [HitBox(diag_offset(size)[0], diag_offset(size)[1], D_HALF + 1, D_HALF + 1)]

    return {
        Entity(Rect(LASER_X, y, height, height), parts=parts, hitboxes=hitboxes),
    }


def make_diagonal2(size: int) -> set[Entity]:
    """A single diagonal laser, bottom-left to top-right"""
    height = D_HALF * 2 + D_HALF * size
    y = generate_y(height)

    # Define frame managers for left, middle, and right parts
    left_frame = make_frame_manager(0, D_BASE_V, TILE_SIZE, 0, D_PART_W, -D_PART_H)
    middle_frame = make_frame_manager(TILE_SIZE * 4, D_BASE_V, TILE_SIZE, 0, D_PART_W, -D_PART_H)
    right_frame = make_frame_manager(0, D_BASE_V, TILE_SIZE, 0, -D_PART_W, D_PART_H)

    # Create parts with frame managers and offsets

    parts = tuple(EntityPart(middle_frame, (D_HALF * m, D_HALF * (size - m))) for m in range(1, size))
    parts += (EntityPart(left_frame, (0, diag_middle_edge(size))),)
    parts += (EntityPart(right_frame, (diag_middle_edge(size), 0)),)

    # Define hitboxes for each section
    hitboxes = [HitBox(D_BASE_HITBOX_OFFSET, diag_offset(size)[1], D_HALF + 1, D_HALF + 1)]
    hitboxes += make_hitboxes(D_HALF, diag_middle_edge(size), D_HALF, -D_HALF, D_HALF, D_HALF, size)
    hitboxes += [(HitBox(diag_offset(size)[0], D_BASE_HITBOX_OFFSET, D_HALF + 1, D_HALF + 1))]

    return {
        Entity(Rect(LASER_X, y, height, height), parts=parts, hitboxes=hitboxes),
    }


def make_diagonals(size: int) -> set[Entity]:
    """An X shape, 2 diagonals laid on top of each other"""
    size = max(2, size)  # Ensure size is bigger than 1 (size 1 looks wierd)
    diag1_entity = next(iter(make_diagonal1(size)))
    diag2_entity = next(iter(make_diagonal2(size)))
    diag2_entity.rect.y = diag1_entity.rect.y
    return {diag1_entity, diag2_entity}


# A laser making function is chosen randomly from here
LASER_MAKERS: tuple[Callable[[int], set[Entity]], ...] = (
    make_horizontal,
    make_vertical,
    make_diagonal1,
    make_diagonal2,
    make_diagonals,
)


def make_laser() -> set[Entity]:
    """
    Generate lasers of random size and alignment.
    The main Entry point.
    """
    size = pyxel.rndi(*LASER_SIZE_BOUNDS)
    laser_maker = LASER_MAKERS[pyxel.rndi(0, len(LASER_MAKERS) - 1)]
    return laser_maker(size)
