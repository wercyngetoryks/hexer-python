from pygame.math import Vector2


class Settings:
    """A class to store all settings"""

    def __init__(self):
        """Initialize the settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.H = 12.68
        self.V = 12.68
        self.factor = 10.92 / 4
        self.hsize = Vector2(self.H * self.factor, self.V * self.factor)
        self.origin = Vector2(600, 400)
        self.offset_x = 30
        self.offset_y = 35
        self.scale = (60, 70)
        self.map_radius = 6
