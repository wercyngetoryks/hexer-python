import sys
import pygame

from settings import Settings
import tilemap
import hex


class Hexer:
    """Class used to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create the game window"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height))

        pygame.display.set_caption("Hexer")

        self.layout = hex.Layout(self.settings.hsize, self.settings.origin)

        self.gameMap = tilemap.Map(self.settings.map_radius, self, self.layout)
        self.gameMap.fill_map()

    def run_game(self):
        """Start the main game loop"""
        while True:
            # Check for keyboard / mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = hex.Point(event.pos[0], event.pos[1])
                    self.gameMap.changeTile(click)

            # Redraw screen background every frame
            self.screen.fill(self.settings.bg_color)
            self.gameMap.drawTiles()

            # Refresh the display
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    h = Hexer()
    h.run_game()
