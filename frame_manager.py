import pyxel
from itertools import cycle

class FrameManager:
    def __init__(self, frames: list, fps=12):
        self.frames = cycle(frames)
        self.frame = next(self.frames)
        self.time = 0
        self.fps = fps
        self.frame_duration = 1 / fps
    
    def update(self, dt):
        self.time += dt
        while self.time > self.frame_duration:
            self.frame = next(self.frames)
            self.time -= self.frame_duration
    
    def draw(self, x, y):
        pyxel.blt(x, y, *self.frame)