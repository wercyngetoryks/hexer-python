import pygame


class Turnsystem():
    """Class used to mae the turn based combat and movement fucking work XD"""

    def __init__(self):
        self.counter = 0
        self.sleep = 100

    def advance(self):
        pygame.time.wait(self.sleep)
        self.counter += 1
