from frame_manager import FrameManager


class PlayerState:
    def __init__(self, player):
        self.player = player

    def draw(self, x, y):
        self.player.frame.draw(x, y)
    
    def update(self):
        self.player.frame.update()


class FlyState(PlayerState):
    FLY_FRAMES = [[0, 16 * i, 0, 16, 16, 3] for i in range(1, 5)]
    def __init__(self, player):
        self.player = player
        self.player.frame = FrameManager(self.FLY_FRAMES)


class RunState(PlayerState):
    RUN_FRAMES = [[0, 16 *i, 16, 16, 16, 3] for i in range(7)]

    def __init__(self, player):
        self.player = player
        self.player.frame = FrameManager(self.RUN_FRAMES, frame_delay=1)