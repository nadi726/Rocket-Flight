import pyxel
from itertools import cycle

class FrameManager:
    def __init__(self, frames: list, frame_delay=2):
        self.frames = cycle(frames)
        self.frame = next(self.frames)
        self.frame_delay = frame_delay
        self.elapsed_frames = 0
    
    def update(self):
        self.elapsed_frames += 1
        if self.elapsed_frames > self.frame_delay:
            self.frame = next(self.frames)
            self.elapsed_frames = 0
    
    def draw(self, x, y):
        pyxel.blt(x, y, *self.frame)