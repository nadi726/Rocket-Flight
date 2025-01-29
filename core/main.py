from enum import Enum

import pyxel

from core import consts
from core.background import Background
from core.entity_manager import EntityManager
from entities.concrete.player import Player


class GameState(Enum):
    START = 1
    PLAYER_ENTERING = 2
    PLAYING = 3
    GAME_OVER = 4


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.load("../resources/res.pyxres")
        self.small_font = pyxel.Font("../resources/spleen-5x8.bdf")
        self.big_font = pyxel.Font("../resources/spleen-8x16.bdf")
        self.reset()
        self.background = Background()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.entity_manager.update_static()
        match self.state:
            case GameState.START:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.state = GameState.PLAYER_ENTERING
                    self.player.start()

            case GameState.PLAYER_ENTERING:
                if self.player.has_finished_entering():
                    self.state = GameState.PLAYING

            case GameState.PLAYING:
                if pyxel.btn(pyxel.KEY_SPACE):
                    self.player.on_key_press()
                self.score += consts.POINTS_PER_FRAME
                self.background.update()
                self.entity_manager.update_scrollables()
                if self.player.is_game_over():
                    self.state = GameState.GAME_OVER

            case GameState.GAME_OVER:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.reset()

    def reset(self):
        self.entity_manager = EntityManager()
        self.player = Player(self.entity_manager)
        self.state: GameState = GameState.START
        self.score: float = 0

    def draw(self):
        self.background.draw()
        self.entity_manager.draw()
        self.player.draw()

        score_text = f"Score: {int(self.score)}"

        # Display score at top left, except in game over state
        # where the score is at the screen's center
        if self.state != GameState.GAME_OVER:
            self.draw_text(30, 1, score_text, self.small_font)

        # Display specific messages based on game state
        if self.state == GameState.START:
            self.draw_centered_text("Press <space> to start", 90, self.big_font)
        elif self.state == GameState.GAME_OVER:
            self.draw_centered_text("Game Over!", 85, self.big_font)
            self.draw_centered_text(score_text, 100, self.small_font)

    def draw_text(self, x: int, y: int, text: str, font: pyxel.Font):
        pyxel.text(x, y, text, 0, font)

    def draw_centered_text(self, text: str, y: int, font: pyxel.Font):
        x = consts.W / 2 - font.text_width(text) / 2
        self.draw_text(int(x), y, text, font)
