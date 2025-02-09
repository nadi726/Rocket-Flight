from pathlib import Path

import pyxel

from . import consts
from .consts import SCROLL_SPEED

BG_SCROLL_SPEED = SCROLL_SPEED // 3


class Background:
    """
    Handles drawing and scrolling the background and foreground(floor) images.
    Background scrolls slower than the foreground for a parallax effect.
    """

    def __init__(self):
        self.bg_img: pyxel.Image = self.load_image("../../resources/background.png")
        self.fg_img: pyxel.Image = self.load_image("../../resources/floor.png")

        self.bg_x: float = 0  # Background position
        self.fg_x: float = 0  # Foreground position
        self.fg_min_x: float = consts.W - self.fg_img.width  # Minimum scroll position
        self.fg_y: float = consts.FLOOR_Y - 1  # y-position of the foreground floor

    @staticmethod
    def load_image(path: str) -> pyxel.Image:
        """Load an image and handle missing files."""
        if not Path(path).exists():
            msg = f"Image not found at {path}"
            raise FileNotFoundError(msg)
        return pyxel.Image.from_image(path)

    def update(self):
        self.fg_x = (self.fg_x - SCROLL_SPEED) % self.fg_min_x
        self.bg_x = (self.bg_x - BG_SCROLL_SPEED) % (-self.bg_img.width)

    def draw(self):
        pyxel.blt(self.bg_x, 0, self.bg_img, 0, 0, self.bg_img.width, self.bg_img.height)
        pyxel.blt(self.bg_x + self.bg_img.width, 0, self.bg_img, 0, 0, self.bg_img.width, self.bg_img.height)
        pyxel.blt(self.fg_x, self.fg_y, self.fg_img, 0, 0, self.fg_img.width, self.fg_img.height)
