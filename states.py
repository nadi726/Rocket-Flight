from typing import TYPE_CHECKING

from frame_manager import Frame, FrameManager

if TYPE_CHECKING:
    from player import Player


class PlayerState:
    def __init__(self, player: "Player"):
        self.player = player

    def draw(self, x: float, y: float):
        self.player.frame.draw(x, y)

    def update(self):
        pass


class FlyState(PlayerState):
    FLY_FRAMES = tuple(Frame(0, 16 * i, 0, 16, 16, 3) for i in range(1, 5))

    def __init__(self, player: "Player"):
        self.player = player
        self.player.frame = FrameManager(self.FLY_FRAMES)


class RunState(PlayerState):
    RUN_FRAMES = tuple(Frame(0, 16 * i, 16, 16, 16, 3) for i in range(7))

    def __init__(self, player: "Player"):
        self.player = player
        self.player.frame = FrameManager(self.RUN_FRAMES, frame_delay=1)
