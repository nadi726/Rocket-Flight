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

    def draw(self):
        self.background.draw()
        self.entity_manager.draw()
        self.player.draw()
        if self.state == GameState.START:
            text = "Press <space> to start"
            x = self.center_text(text)
            pyxel.text(x, 90, text, 0, None)
        if self.state == GameState.GAME_OVER:
            text = "You lose!"
            x = self.center_text(text)
            pyxel.text(x, 90, text, 0, None)

    def center_text(self, text: str):
        return consts.W / 2 - len(text) / 2 * 4
