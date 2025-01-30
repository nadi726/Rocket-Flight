from typing import TYPE_CHECKING, NamedTuple

import pyxel

from core.consts import CEILING_Y, FLOOR_Y, TILE_SIZE
from core.frame_manager import Frame, FrameManager
from entities.entity import Entity, Rect

if TYPE_CHECKING:
    from core.entity_manager import EntityManager


class PlayerState:
    """
    Base class for player states.

    Provides basic methods expected of a player state.
    """

    @staticmethod
    def enter(player: "Player"):
        """Called when entering the state."""

    @staticmethod
    def update(player: "Player"):
        """Called every frame to update the player's state."""

    @staticmethod
    def on_key_press(player: "Player"):
        """Called when a key is pressed."""


class PlayerStartState(PlayerState):
    @staticmethod
    def enter(player: "Player"):
        player.frame_manager = player.FRAME_MANAGERS.run
        player.rect.right = 0
        player.rect.bottom = FLOOR_Y - 1
        player.vx = player.ENTER_VX

    @staticmethod
    def update(player: "Player"):
        # Once the player reaches the playing position, he's ready to play
        if player.rect.x >= player.PLAY_X:
            player.set_state(PlayerPlayState)


class PlayerPlayState(PlayerState):
    @staticmethod
    def enter(player: "Player"):
        player.rect.x = player.PLAY_X
        player.vx = 0

    @staticmethod
    def update(player: "Player"):
        # handle floor
        if player.rect.bottom >= FLOOR_Y:
            player.rect.bottom = FLOOR_Y - 1
            player.vy = 0
            player.ay = 0
            player.frame_manager = player.FRAME_MANAGERS.run
            player.is_flying = False
        # handle ceiling
        if player.rect.top <= CEILING_Y:
            player.rect.top = CEILING_Y
            player.vy = max(0, player.vy)

        if player.key_is_pressed:
            player.fly()
        else:
            player.fall()


class PlayerGameOverState(PlayerState):
    @staticmethod
    def enter(player: "Player"):
        player.vx = player.GAMEOVER_VELOCITY[0]
        player.vy = player.GAMEOVER_VELOCITY[1]
        player.ay = player.FALL_ACCELERATION
        player.frame_manager = player.FRAME_MANAGERS.gameover

    @staticmethod
    def update(player: "Player"):
        if player.rect.bottom > player.GAMEOVER_Y:
            player.rect.bottom = Player.GAMEOVER_Y
            player.vy = 0
            player.ay = 0
            # Player slides after falling
            player.ax = player.GAMEOVER_SLIDE_ACCELERATION

        player.vx = max(0, player.vx)


class FrameManagerRecord(NamedTuple):
    """A record of FrameManagers for the player's different states."""

    fly: FrameManager
    fall: FrameManager
    run: FrameManager
    gameover: FrameManager


class Player(Entity):
    W = 12
    H = 16
    ENTER_VX = 2
    MAX_SPEED = 6
    PLAY_X = 40
    JETPACK_ACCELERATION = -0.4
    FALL_ACCELERATION = 0.5

    GAMEOVER_Y = FLOOR_Y + 5
    GAMEOVER_VELOCITY = (3, -3)
    GAMEOVER_SLIDE_ACCELERATION = -0.1

    FRAME_MANAGERS = FrameManagerRecord(
        fly=FrameManager(tuple(Frame(0, TILE_SIZE * i, 0, TILE_SIZE, TILE_SIZE) for i in range(1, 5))),
        fall=FrameManager((Frame(0, TILE_SIZE * 3, TILE_SIZE, TILE_SIZE, TILE_SIZE),)),
        run=FrameManager(tuple(Frame(0, TILE_SIZE * i, TILE_SIZE, TILE_SIZE, TILE_SIZE) for i in range(7))),
        gameover=FrameManager((Frame(0, TILE_SIZE * 7, TILE_SIZE, TILE_SIZE, TILE_SIZE),)),
    )

    def __init__(self, entity_manager: "EntityManager"):
        super().__init__(Rect(0, 0, Player.W, Player.H))
        self.ay: float = 0.0
        self.ax: float = 0.0
        self.entity_manager = entity_manager
        self.set_state(PlayerState) # Acts as a placeholder state
        self.coins = 0
        self.key_is_pressed = False
        self.is_flying = False

    def update(self):
        super().update()
        self.vy += max(min(self.ay, self.MAX_SPEED), -self.MAX_SPEED)
        self.vx += min(self.ax, self.MAX_SPEED)
        self.state.update(self)
        self.key_is_pressed = False

    def collect_coins(self):
        coins = self.coins
        self.coins = 0
        return coins

    def fly(self):
        if not self.is_flying:
            self.ay = self.JETPACK_ACCELERATION
            self.frame_manager = self.FRAME_MANAGERS.fly
            self.is_flying = True
        if pyxel.frame_count % 3 == 0:
            self.entity_manager.make_player_bullets(self.rect)

    def fall(self):
        if self.is_flying:
            self.ay = self.FALL_ACCELERATION
            self.frame_manager = self.FRAME_MANAGERS.fall
            self.is_flying = False

    def set_state(self, state: type[PlayerState]):
        self.state = state
        self.state.enter(self)

    def start(self):
        self.set_state(PlayerStartState)

    def on_key_press(self):
        self.key_is_pressed = True

    def has_finished_entering(self) -> bool:
        return self.state == PlayerPlayState

    def is_game_over(self):
        return self.state == PlayerGameOverState

    def game_over(self):
        self.set_state(PlayerGameOverState)
