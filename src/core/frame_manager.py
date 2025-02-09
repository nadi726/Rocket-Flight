from dataclasses import asdict, dataclass
from itertools import cycle

import pyxel

from .consts import IMG_COLKEY


@dataclass
class Frame:
    img: int | pyxel.Image
    u: float
    v: float
    w: float
    h: float
    colkey: int | None = IMG_COLKEY
    rotate: float | None = None
    scale: float | None = None

    @staticmethod
    def empty():
        """Create an empty Frame with default values."""
        return Frame(0, 0, 0, 0, 0)


class FrameManager:
    def __init__(self, frames: tuple["Frame", ...], frame_delay: int = 2):
        self.frames = cycle(frames)
        self.frame: Frame = next(self.frames)
        self.frame_delay: int = frame_delay
        self.elapsed_frames: int = 0

    def update(self):
        self.elapsed_frames += 1
        if self.elapsed_frames >= self.frame_delay:
            self.frame = next(self.frames)
            self.elapsed_frames = self.elapsed_frames - self.frame_delay

    def draw(self, x: float, y: float):
        pyxel.blt(x, y, **asdict(self.frame))

    @staticmethod
    def empty() -> "FrameManager":
        return FrameManager((Frame.empty(),))
