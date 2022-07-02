from math import sqrt


class HexDirections():
    """Class used solely to store 6 move vectors on hexagonal grid made of POINT TOP hexagons."""

    def __init__(self):
        self.E = (1, 0, -1)
        self.NE = (1, -1, 0)
        self.NW = (0, -1, 1)
        self.W = (-1, 0, 1)
        self.SW = (-1, 1, 0)
        self.SE = (0, 1, -1)


class Orientation():
    """Class storing matrices for hex calculations"""

    def __init__(self):
        self.f0 = sqrt(3)
        self.f1 = sqrt(3) / 2
        self.f2 = 0
        self.f3 = 3 / 2
        self.b0 = sqrt(3) / 3
        self.b1 = -1 / 3
        self.b2 = 0
        self.b3 = 2 / 3


class Point():
    """A simple point class."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pixel_to_hex(self, layout):
        """Returns a Hex() coordinate from a given point."""
        matrix = layout.orientation
        new_x = (self.x - layout.origin.x) / layout.size.x
        new_y = (self.y - layout.origin.y) / layout.size.y

        q = matrix.b0 * new_x + matrix.b1 * new_y
        r = matrix.b2 * new_x + matrix.b3 * new_y
        s = -q - r

        q_r = round(q)
        r_r = round(r)
        s_r = round(s)

        q_diff = abs(q_r - q)
        r_diff = abs(r_r - r)
        s_diff = abs(s_r - s)

        if q_diff > r_diff and q_diff > s_diff:
            q_r = -r_r - s_r
        elif r_diff > s_diff:
            r_r = -q_r - s_r
        else:
            s_r = -q_r - r_r

        return Hex(q_r, r_r, s_r)


class Layout():
    """Class used for calculating hex to pixel and pixel to hex"""

    def __init__(self, size, origin):
        self.orientation = Orientation()
        self.size = size
        self.origin = origin


class Hex():
    """Class representing cube hexagonal coordinates."""

    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        assert self.q + self.r + \
            self.s == 0, f"Hex coordinates must sum to 0, but now it's {self.q + self.r + self.s}."

    def __eq__(self, other):
        """Function used to compare hex coordinates."""
        return self.q == other.q and self.r == other.r and self.s == other.s

    # Functions used to perform coordinate arithmetic

    def hex_add(self, other):
        """Function for adding two hex coordinates."""
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def hex_subtract(self, other):
        """Function for substracting 'other' from 'self' coordinates."""
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def hex_multiply(self, other):
        """Function for multiplying two hex coordinates."""
        return Hex(self.q * other.q, self.r * other.r, self.s * other.s)

    # Functions calculating distance:

    def hex_lenght(self):
        """Returns distance (number of steps) from Hex(0, 0, 0)."""
        return int((abs(self.q) + abs(self.r) + abs(self.s)) / 2)

    def hex_distance(self, other):
        """Returns distance (number of steps) from one hex coordinate to the other."""
        dis = self.hex_subtract(other)
        return (abs(dis.q) + abs(dis.r) + abs(dis.s)) / 2

    # Instantiate HexDirections
    dirs = HexDirections()

    def hex_neighbor(self, direction):
        """Returns coordinates of neighboring hexagon in a given direction (using self.dirs.<direction>"""
        return self.hex_add(direction)

    def hex_to_pixel(self, layout):
        matrix = layout.orientation
        x = (matrix.f0 * self.q + matrix.f1 * self.r) * layout.size.x
        y = (matrix.f2 * self.q + matrix.f3 * self.r) * layout.size.y

        return Point(x + layout.origin.x, y + layout.origin.y)
