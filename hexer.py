import sys
import pygame
import pygame_gui as pgui

from settings import Settings
import tilemap
import hex


class Hexer:
    """Class used to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create the game window"""
        pygame.init()
        self.counter = 0
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height))

        self.manager = pgui.UIManager(
            (self.settings.screen_width, self.settings.screen_height), 'theme.json')

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Hexer")

        self.gameMap = tilemap.Map(self.settings.map_radius, self)
        self.gameMap.fill_map()

        self.initialize_UI()

    def initialize_UI(self):
        """Initializes all starting UI elements"""
        self.quit_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 10), (90, 40)), text='Quit', manager=self.manager)
        self.turn_advance_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 60), (90, 40)), text='Advance turn', manager=self.manager)
        self.healthbar = pgui.elements.UIProgressBar(
            relative_rect=pygame.Rect((890, 10), (300, 40)), manager=self.manager)
        self.healthbar.set_current_progress(100)
        self.turn_counter = pgui.elements.UILabel(relative_rect=pygame.Rect(
            (1090, 60), (100, 20)), manager=self.manager, text=f"{self.counter}")

    def advance(self):
        self.counter += 1
        pygame.time.delay(100)

    def run_game(self):
        """Start the main game loop"""

        while True:
            self.gameMap.update()
            # Check for keyboard / mouse events
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.manager.process_events(event)

            self.manager.update(time_delta)

            mousepos = hex.Point(pygame.mouse.get_pos()[
                                 0], pygame.mouse.get_pos()[1])
            self.gameMap.highlightTile(mousepos)

            # Redraw screen background every frame
            self.screen.fill(self.settings.bg_color)
            self.gameMap.drawTiles()
            self.turn_counter.set_text(f"{self.counter}")
            self.manager.draw_ui(self.screen)

            # Refresh the display
            pygame.display.flip()
