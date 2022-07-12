import hex

import pygame


class Sprite(hex.Hex):
    """Class for handling both Player and Enemy subclasses later on."""

    def __init__(self, q, r, s, h_game):
        super().__init__(q, r, s)
        self.hp = 100
        self.alive = True
        self.range = 1
        self.screen = h_game.screen
        self.layout = h_game.layout
        # mage as a placeholder of sorts
        self.image = pygame.image.load(
            r"D:\!Programming shit\PYTHON\hexer-python\images\sprites\mage.png")
        self.turns = h_game.turns

    def move(self, click):
        position = click.pixel_to_hex(self.layout)
        if self.hex_distance(position) <= self.range:
            self.q, self.r, self.s = position.q, position.r, position.s
            self.turns.advance()

    def draw(self):
        position = self.hex_to_pixel(self.layout)
        self.screen.blit(self.image, (position.x - 16, position.y - 17))


class Player(Sprite):
    """Class for handling player character, movement, health and so on."""

    def __init__(self, q, r, s, h_game):
        super().__init__(q, r, s, h_game)
