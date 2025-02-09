from collections.abc import Callable
from enum import Enum

import pyxel

from core import consts
from core.background import Background
from core.entity_manager import EntityManager
from core.sounds import sounds
from entities.concrete.player import Player
from entities.entity import Rect


class GameState(Enum):
    START = 1
    PLAYER_ENTERING = 2
    PLAYING = 3
    GAME_OVER = 4


class App:
    def __init__(self):
        pyxel.init(consts.W, consts.H)
        pyxel.title("Rocket Flight")
        pyxel.load("../resources/res.pyxres")

        self.small_font = pyxel.Font("../resources/spleen-5x8.bdf")
        self.big_font = pyxel.Font("../resources/spleen-8x16.bdf")
        self.music_button = MusicButton(110, 1, self.small_font)

        self.background = Background()
        self.high_score = 0
        self.reset()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.music_button.update()

        self.player.update()
        self.entity_manager.update_static()

        match self.state:
            case GameState.START:
                if self.action_input_pressed():
                    sounds.transition()
                    self.player.start()
                    self.state = GameState.PLAYER_ENTERING

            case GameState.PLAYER_ENTERING:
                if self.player.has_finished_entering():
                    self.state = GameState.PLAYING

            case GameState.PLAYING:
                self.update_playing()

            case GameState.GAME_OVER:
                if self.score > self.high_score:
                    self.new_high_score = True
                    self.high_score = self.score

                if self.action_input_pressed():
                    sounds.transition()
                    self.reset()

    def update_playing(self):
        if self.action_input_held():
            self.player.on_key_press()

        self.update_score()
        self.background.update()
        self.entity_manager.update_scrollables(self.player)

        if self.player.is_game_over():
            self.state = GameState.GAME_OVER

    def update_score(self):
        self.score += consts.POINTS_PER_FRAME
        self.score += self.player.collect_coins() * consts.POINTS_PER_COIN
        self.score += self.entity_manager.collect_dead_scientists() * consts.POINTS_PER_SCIENTIST

    def _is_action_input(self, btn_func: Callable[[int], bool]):
        return btn_func(pyxel.KEY_SPACE) or (pyxel.mouse_y >= consts.CEILING_Y and btn_func(pyxel.MOUSE_BUTTON_LEFT))

    def action_input_pressed(self):
        return self._is_action_input(pyxel.btnp)

    def action_input_held(self):
        return self._is_action_input(pyxel.btn)

    def reset(self):
        self.entity_manager = EntityManager()
        self.player = Player(self.entity_manager)
        self.state: GameState = GameState.START
        self.score: float = 0
        self.new_high_score = False

    def draw(self):
        self.background.draw()
        self.music_button.draw()
        self.entity_manager.draw()
        self.player.draw()

        score_text = f"Score: {int(self.score)}"
        # Display score at top left, except in game over state
        # where the score is at the screen's center
        self.draw_text(10, 1, score_text, self.small_font)
        self.draw_text(240, 1, f"Best: {int(self.high_score)}", self.small_font)

        # Display specific messages based on game state
        if self.state == GameState.START:
            self.draw_centered_text("Rocket Flight", 80, self.big_font)
            self.draw_centered_text("Press <space> or click to start", 100, self.small_font)
        elif self.state == GameState.GAME_OVER:
            self.draw_centered_text("Game Over!", 85, self.big_font)
            self.draw_centered_text(score_text, 100, self.small_font)
            if self.new_high_score:
                self.draw_centered_text("New high score!!!", 115, self.small_font)

    def draw_text(self, x: int, y: int, text: str, font: pyxel.Font):
        pyxel.text(x, y, text, 0, font)

    def draw_centered_text(self, text: str, y: int, font: pyxel.Font):
        x = consts.W / 2 - font.text_width(text) / 2
        self.draw_text(int(x), y, text, font)


class MusicButton:
    """
    A button for toggling music playback.
    """

    MAIN_TEXT = "Music <M>"
    ON_TEXT = "[ON]"
    OFF_TEXT = "[OFF]"

    def __init__(self, x: float, y: float, font: pyxel.Font):
        self.is_music_playing = False
        self._toggle_music()

        self.font = font
        self.rect = Rect(x, y, font.text_width(self._get_text()), 8)

    def _get_text(self):
        state_text = self.ON_TEXT if self.is_music_playing else self.OFF_TEXT
        return f"{state_text} {self.MAIN_TEXT}"

    def _toggle_music(self):
        if self.is_music_playing:
            for channel in range(3):
                pyxel.stop(channel)
        else:
            pyxel.playm(0, loop=True)
        self.is_music_playing = not self.is_music_playing

    def _in_bounds(self):
        return self.rect.right >= pyxel.mouse_x >= self.rect.left and self.rect.bottom >= pyxel.mouse_y >= self.rect.top

    def update(self):
        if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self._in_bounds()) or pyxel.btnp(pyxel.KEY_M):
            self._toggle_music()

    def draw(self):
        pyxel.text(self.rect.x, self.rect.y, self._get_text(), 0, self.font)
