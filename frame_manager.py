import pyxel
from itertools import cycle
from dataclasses import dataclass, asdict


class FrameManager:
    def __init__(self, frames: tuple, frame_delay=2):
        self.frames = cycle(frames)
        self.frame = next(self.frames)
        self.frame_delay = frame_delay
        self.elapsed_frames = 0
    
    def update(self):
        self.elapsed_frames += 1
        if self.elapsed_frames >= self.frame_delay:
            self.frame = next(self.frames)
            self.elapsed_frames = self.elapsed_frames - self.frame_delay

    def draw(self, x, y):
        if isinstance(self.frame, Frame):
            frame = asdict(self.frame)
            pyxel.blt(x, y, **frame)
        else: 
            pyxel.blt(x, y, *self.frame)


@dataclass
class Frame:
    img: int | pyxel.Image
    u : float
    v : float
    w : float
    h : float
    colkey : int | None = None
    rotate : float | None = None
    scale : float | None = None

    @staticmethod
    def empty():
        """Create an empty Frame with default values."""
        return Frame(0, 0, 0, 0, 0)