import pygame

import hex


class Player(pygame.sprite.Sprite):
    """Class for handling the player, inherits from pygame.sprite.Sprite class."""

    def __init__(self, x, y, z):
        super().__init__()
        # Instance of Hex class for coordinates
        self.position = hex.Hex(x, y, z)
        # Load a player sprite
        self.image = pygame.image.load(
            'images/sprites/mage.png').convert_alpha()
        self.update_pixel_position()
        # Set current health and health capacity for the healthbar
        self.current_health = 100
        self.health_capacity = 100

    def move(self, x, y):
        click = hex.Point(x, y)
        move_to = click.pixel_to_hex()
        if self.position.hex_distance(move_to) == 1:
            self.position = move_to
            self.update_pixel_position()

    def update_pixel_position(self):
        self.pixel_coordinates = self.position.hex_to_pixel()
        self.rect = self.image.get_rect(bottomleft=(
            self.pixel_coordinates.x - 16, self.pixel_coordinates.y + 17))
