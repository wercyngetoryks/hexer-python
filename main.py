import sys
import pygame
import pygame_gui as pgui

from settings import Settings
import tilemap
import hex
import sprite
from turnsystem import Turnsystem


class Hexer:
    """Class used to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create the game window"""
        pygame.init()
        self.turns = Turnsystem()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height))

        self.manager = pgui.UIManager(
            (self.settings.screen_width, self.settings.screen_height))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Hexer")

        self.layout = hex.Layout(self.settings.hsize, self.settings.origin)

        self.gameMap = tilemap.Map(self.settings.map_radius, self, self.layout)
        self.gameMap.fill_map()

        self.initialize_UI()

        self.player = sprite.Player(0, 0, 0, self)

    def initialize_UI(self):
        """Initializes all starting UI elements"""
        self.quit_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 10), (90, 40)), text='Quit', manager=self.manager)
        self.turn_advance_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 60), (90, 40)), text='Advance turn', manager=self.manager)
        self.healthbar = pgui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((890, 10), (300, 40)), manager=self.manager)
        self.turn_counter = pgui.elements.UILabel(relative_rect=pygame.Rect(
            (1090, 60), (100, 20)), manager=self.manager, text=f"{self.turns.counter}")

    def run_game(self):
        """Start the main game loop"""

        while True:
            # Check for keyboard / mouse events
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.manager.process_events(event)

                if event.type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = hex.Point(event.pos[0], event.pos[1])
                        self.player.move(click)

            self.manager.update(time_delta)

            mousepos = hex.Point(pygame.mouse.get_pos()[
                                 0], pygame.mouse.get_pos()[1])
            self.gameMap.highlightTile(mousepos)

            # Redraw screen background every frame
            self.screen.fill(self.settings.bg_color)
            self.gameMap.drawTiles()
            self.player.draw()
            self.turn_counter.set_text(f"{self.turns.counter}")
            self.manager.draw_ui(self.screen)

            # Refresh the display
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    h = Hexer()
    h.run_game()
