import pyxel


class _Sounds:
    FLY_SOUND_TIMEOUT = 4

    def __init__(self):
        self._last_frame_played = 0

    def transition(self):
        """
        Called when changing from main screen to playing mode, and from game over back to main screen.
        """
        pyxel.play(3, 61)

    def fly(self):
        if pyxel.frame_count - self._last_frame_played > self.FLY_SOUND_TIMEOUT:
            pyxel.play(3, 63)
            self._last_frame_played = pyxel.frame_count

    def catch_coin(self):
        pyxel.play(3, 60)

    def hit_scientist(self):
        pyxel.play(3, 59)

    def game_over(self):
        pyxel.play(3, 62)


sounds = _Sounds()
