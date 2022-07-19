from enum import Enum
import pygame

import hex
from settings import Settings


class TileState(Enum):
    CLEAR = 0
    CURSED = 1
    BLESSED = 2
    DESTROYED = 3


class Tile(pygame.sprite.Sprite):
    """Class representing a map tile with it's properties. Inherits from pygame.sprite.Sprite and uses Hex to represent coordinates."""

    def __init__(self, x, y, z):
        super().__init__()
        self.position = hex.Hex(x, y, z)
        self.state = TileState.CLEAR
        self.image = pygame.image.load('images/tiles/grass_2.png').convert()
        self.image = pygame.transform.scale(self.image, self.settings.scale)
        self.highlighted = False
        self.lastSpell = 0

    settings = Settings()

    def set_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, self.settings.scale)
        pixel_position = self.position.hex_to_pixel()
        self.rect = self.image.get_rect(bottomleft=(
            pixel_position.x - self.settings.offset_x, pixel_position.y + self.settings.offset_y))


class Map():
    """Class used for storage of Tile objects."""

    def __init__(self, radius, h_game):
        self.radius = radius
        self.screen = h_game.screen
        self.layout = hex.Layout()
        self.hTile = hex.Hex(0, 0, 0)
        self.prev_hTile = hex.Hex(0, 0, 0)

    settings = Settings()

    tilemap = {}

    def fill_map(self):
        """Fill a map with tiles arranged in a hexagonal shape with a radius specified when instantiating a Map."""
        tiles = pygame.sprite.Group()
        for x in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -x - self.radius)
            r2 = min(self.radius, -x + self.radius)
            for y in range(r1, r2 + 1):
                newtile = Tile(x, y, -x - y)
                self.tilemap[(newtile.position.x,
                              newtile.position.y)] = newtile
                tiles.add(newtile)
        return tiles

    def highlightTile(self, x, y):
        """Sets tile flag as highlighted"""
        click = hex.Point(x, y)
        looking = click.pixel_to_hex()
        try:
            self.prev_hTile = self.hTile
            self.hTile = looking
            self.tilemap[(self.hTile.x, self.hTile.y)].highlighted = True
            if self.prev_hTile != self.hTile:
                self.tilemap[(self.prev_hTile.x, self.prev_hTile.y)
                             ].highlighted = False
        except KeyError:
            for tile in self.tilemap.values():
                tile.highlighted = False

    def curseTile(self, x, y):
        """Converts a normal tile to a cursed tile on click."""
        click = hex.Point(x, y)
        looking = click.pixel_to_hex()
        try:
            self.tilemap[(looking.x, looking.y)].state = TileState.CURSED
        except KeyError:
            pass

    def update(self):
        # for tile in self.tilemap.values():
        #     if tile.state == TileState.CURSED:
        #         tile.state = TileState.CLEAR

        for tile in self.tilemap.values():
            if tile.state == TileState.CLEAR:
                if tile.highlighted is True:
                    tile.set_image('images/tiles/h_grass.png')
                else:
                    tile.set_image('images/tiles/grass_2.png')
            elif tile.state == TileState.CURSED:
                if tile.highlighted is True:
                    tile.set_image('images/tiles/h_cursed.png')
                else:
                    tile.set_image('images/tiles/cursed_2.png')
