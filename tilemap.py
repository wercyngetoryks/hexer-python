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

    def __init__(self, x, y, z, h_game):
        super().__init__(x, y, z)
        self.state = TileState.CLEAR
        self.screen = h_game.screen
        self.image = pygame.image.load('images/tiles/grass.png')
        self.image = pygame.transform.scale(self.image, self.settings.scale)
        self.highlighted = False
        self.lastSpell = 0

    settings = Settings()

    def set_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, self.settings.scale)


class Map():
    """Class used for storage of Tile objects."""

    def __init__(self, radius, h_game):
        self.radius = radius
        self.h_game = h_game
        self.layout = hex.Layout()
        self.hTile = hex.Hex(0, 0, 0)
        self.prev_hTile = hex.Hex(0, 0, 0)

    settings = Settings()

    tilemap = {}

    def fill_map(self):
        """Fill a map with tiles arranged in a hexagonal shape with a radius specified when instantiating a Map."""
        for x in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -x - self.radius)
            r2 = min(self.radius, -x + self.radius)
            for y in range(r1, r2 + 1):
                print(y)
                newtile = Tile(x, y, -x - y, self.h_game)
                self.tilemap[(newtile.x, newtile.y)] = newtile
        # print(self.tilemap)

    def drawTiles(self):
        """Draws all tiles stored in the dictionary"""
        for tile in self.tilemap.values():
            position = tile.hex_to_pixel()
            tile.screen.blit(
                tile.image, (position.x - self.settings.offset_x, position.y - self.settings.offset_y))

    def highlightTile(self, position):
        """Sets tile flag as highlighted"""
        looking = position.pixel_to_hex()
        try:
            self.prev_hTile = self.hTile
            self.hTile = looking
            self.tilemap[(self.hTile.x, self.hTile.y)].highlighted = True
            if self.prev_hTile != self.hTile:
                self.tilemap[(self.prev_hTile.x, self.prev_hTile.y)].highlighted = False
        except KeyError:
            for tile in self.tilemap.values():
                tile.highlighted = False

    def curseTile(self, position):
        """Converts a normal tile to a cursed tile on click."""
        looking = position.pixel_to_hex()
        try:
            self.tilemap[(looking.x, looking.y)].state = TileState.CURSED
            self.tilemap[(looking.x, looking.y)].lastSpell = self.h_game.counter
            self.h_game.advance()
        except KeyError:
            pass

    def update(self):
        for tile in self.tilemap.values():
            if tile.state == TileState.CURSED and self.h_game.counter - tile.lastSpell > 3:
                tile.state = TileState.CLEAR

        for tile in self.tilemap.values():
            if tile.state == TileState.CLEAR:
                if tile.highlighted is True:
                    tile.set_image('images/tiles/highlighted_grass.png')
                else:
                    tile.set_image('images/tiles/grass.png')
            elif tile.state == TileState.CURSED:
                if tile.highlighted is True:
                    tile.set_image('images/tiles/highlighted_cursed.png')
                else:
                    tile.set_image('images/tiles/cursed.png')
