from enum import Enum
import pygame

import hex
from settings import Settings


class TileState(Enum):
    CLEAR = 0
    CURSED = 1
    BLESSED = 2
    DESTROYED = 3


class Tile(hex.Hex):
    """Class representing a map tile with it's properties. Inherits from Hex() to represent coordinates."""
    def __init__(self, q, r, s, state, h_game):
        super().__init__(q, r, s)
        self.state = state
        self.screen = h_game.screen
        self.image = pygame.image.load('images/tiles/basic_stone.png')
        self.image = pygame.transform.scale(self.image, self.settings.scale)

    settings = Settings()

    def set_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, self.settings.scale)


class Map():
    """Class used for storage of Tile objects."""
    def __init__(self, radius, h_game, layout):
        self.radius = radius
        self.h_game = h_game
        self.layout = layout

    settings = Settings()

    tilemap = []

    def fill_map(self):
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                self.tilemap.append(Tile(q, r, -q - r, TileState.CLEAR, self.h_game))

    def drawTiles(self):
        for tile in self.tilemap:
            position = tile.hex_to_pixel(self.layout)
            tile.screen.blit(tile.image, (position.x - self.settings.offset_x, position.y - self.settings.offset_y))

    def changeTile(self, click):
        print(click.x, click.y)
        looking = click.pixel_to_hex(self.layout)
        print(looking.q, looking.r, looking.s)
        for tile in self.tilemap:
            if looking.q == tile.q and looking.r == tile.r:
                tile.set_image('images/tiles/black_stone.png')
