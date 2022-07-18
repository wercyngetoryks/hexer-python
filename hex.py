from math import sqrt

import pygame
from settings import Settings

settings = Settings()

HexDirections = {
    'E': pygame.math.Vector3(1, 0, -1),
    'NE': pygame.math.Vector3(1, -1, 0),
    'NW': pygame.math.Vector3(0, -1, 1),
    'W': pygame.math.Vector3(-1, 0, 1),
    'SW': pygame.math.Vector3(-1, 1, 0),
    'SE': pygame.math.Vector3(0, 1, -1)}


class Orientation():
    """Class storing matrices for hex calculations"""
    f0 = sqrt(3)
    f1 = sqrt(3) / 2
    f2 = 0
    f3 = 3 / 2
    b0 = sqrt(3) / 3
    b1 = -1 / 3
    b2 = 0
    b3 = 2 / 3


class Layout():
    """Class used for calculating hex to pixel and pixel to hex"""

    def __init__(self):
        self.orientation = Orientation()
        self.size = settings.hsize
        self.origin = settings.origin


class Point(pygame.math.Vector2):
    """A simple point class."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.layout = Layout()

    def pixel_to_hex(self):
        """Returns a Hex() coordinate from a given point."""
        matrix = self.layout.orientation
        new_x = (self.x - self.layout.origin.x) / self.layout.size.x
        new_y = (self.y - self.layout.origin.y) / self.layout.size.y

        x = matrix.b0 * new_x + matrix.b1 * new_y
        y = matrix.b2 * new_x + matrix.b3 * new_y
        z = -x - y

        x_r = round(x)
        y_r = round(y)
        z_r = round(z)

        x_diff = abs(x_r - x)
        y_diff = abs(y_r - y)
        z_diff = abs(z_r - z)

        if x_diff > y_diff and x_diff > z_diff:
            x_r = -y_r - z_r
        elif y_diff > z_diff:
            y_r = -x_r - z_r
        else:
            z_r = -x_r - y_r

        return Hex(x_r, y_r, z_r)


class Hex(pygame.math.Vector3):
    """Class representing cube hexagonal coordinates, based on pygame Vector3 class."""

    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.layout = Layout()
        assert self.x + self.y + \
            self.z == 0, f"Hex coordinates must sum to 0, but now it's {self.x + self.y + self.z}."

    def hex_length(self):
        """Returns the lenght of the vector."""
        return self.length() / 2

    def hex_distance(self, other):
        """Returns distance between self and other hexagon."""
        return self.distance_to(other) / 2

    def hex_neighbor(self, direction):
        """Returns coordinates of neighboring hexagon in a given direction using the HexDirections dictionary."""
        return self + HexDirections[direction]

    def hex_to_pixel(self):
        matrix = self.layout.orientation
        x = (matrix.f0 * self.x + matrix.f1 * self.y) * self.layout.size.x
        y = (matrix.f2 * self.x + matrix.f3 * self.y) * self.layout.size.y

        return Point(x + self.layout.origin.x, y + self.layout.origin.y)
