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
        self.image = pygame.image.load('images/tiles/grass.png')
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
        self.hTile = hex.Hex(0, 0, 0)
        self.prev_hTile = hex.Hex(0, 0, 0)

    settings = Settings()

    tilemap = {}

    def fill_map(self):
        """Fill a map with tiles arranged in a hexagonal shape with a radius specified when instantiating a Map."""
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                newtile = Tile(q, r, -q - r, TileState.CLEAR, self.h_game)
                self.tilemap[(newtile.q, newtile.r)] = newtile
        # print(self.tilemap)

    def drawTiles(self):
        """Draws all tiles stored in the dictionary"""
        for tile in self.tilemap.values():
            position = tile.hex_to_pixel(self.layout)
            tile.screen.blit(
                tile.image, (position.x - self.settings.offset_x, position.y - self.settings.offset_y))

    def highlightTile(self, position):
        """Stores tile at current mouse position as self.hTile, stores previous hTile. Highlights and removes highlights."""
        looking = position.pixel_to_hex(self.layout)
        try:
            self.prev_hTile = self.hTile
            self.hTile = looking
            self.tilemap[(self.hTile.q, self.hTile.r)].set_image('images/tiles/highlighted_grass.png')
            if self.prev_hTile != self.hTile:
                self.tilemap[(self.prev_hTile.q, self.prev_hTile.r)].set_image('images/tiles/grass.png')
        except KeyError:
            for tile in self.tilemap.values():
                tile.set_image('images/tiles/grass.png')
