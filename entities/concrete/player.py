from typing import TYPE_CHECKING

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
        player.frame_manager = FrameManager(player.RUN_FRAMES)
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
        # if the player has landed, make him run
        if player.rect.bottom >= FLOOR_Y:
            player.rect.bottom = FLOOR_Y - 1
            player.vy = 0
            player.ay = 0
            player.frame_manager = FrameManager(player.RUN_FRAMES)

        for entity in player.entity_manager.entities:
            if player.collides(entity) and player.entity_manager.is_hazard(entity):
                player.set_state(PlayerFallState)

    @staticmethod
    def on_key_press(player: "Player"):
        player.vy = player.START_VY
        if player.ay == 0:  # if player is not flying, make him fly
            player.ay = player.GRAVITY
            player.frame_manager = FrameManager(player.FLY_FRAMES)
        if pyxel.frame_count % 3 == 0:
            player.entity_manager.make_player_bullets(player.rect)


class PlayerFallState(PlayerState):
    @staticmethod
    def enter(player: "Player"):
        player.vx = player.FALL_VELOCITY[0]
        player.vy = player.FALL_VELOCITY[1]
        player.ay = player.GRAVITY
        player.frame_manager = FrameManager(player.FALL_FRAMES)

    @staticmethod
    def update(player: "Player"):
        if player.rect.bottom > player.FALL_Y:
            player.rect.bottom = Player.FALL_Y
            player.vy = 0
            player.ay = 0
            # Player slides after falling
            player.ax = player.FALL_SLIDE_ACCELERATION

        player.vx = max(0, player.vx)


class Player(Entity):
    W = 12
    H = 16
    ENTER_VX = 2
    MAX_SPEED = 300
    START_VY = -3
    PLAY_X = 40
    GRAVITY = 0.3
    FALL_Y = FLOOR_Y + 5
    FALL_VELOCITY = (3, -3)
    FALL_SLIDE_ACCELERATION = -0.1

    FLY_FRAMES = tuple(Frame(0, TILE_SIZE * i, 0, TILE_SIZE, TILE_SIZE) for i in range(1, 5))
    RUN_FRAMES = tuple(Frame(0, TILE_SIZE * i, TILE_SIZE, TILE_SIZE, TILE_SIZE) for i in range(7))
    FALL_FRAMES = (Frame(0, TILE_SIZE * 7, TILE_SIZE, TILE_SIZE, TILE_SIZE),)

    def __init__(self, entity_manager: "EntityManager"):
        super().__init__(Rect(0, 0, Player.W, Player.H))
        self.ay: float = 0.0
        self.ax: float = 0.0
        self.entity_manager = entity_manager
        self.set_state(PlayerState)

    def update(self):
        super().update()
        self.vy += min(self.ay, self.MAX_SPEED)
        self.vx += min(self.ax, self.MAX_SPEED)
        self.rect.y = max(CEILING_Y, self.rect.y)
        self.state.update(self)

    def set_state(self, state: type[PlayerState]):
        self.state = state
        self.state.enter(self)

    def start(self):
        self.set_state(PlayerStartState)

    def on_key_press(self):
        self.state.on_key_press(self)

    def has_finished_entering(self) -> bool:
        return self.state == PlayerPlayState

    def is_game_over(self):
        return self.state == PlayerFallState

    def game_over(self):
        self.set_state(PlayerFallState)
