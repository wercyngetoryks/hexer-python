import sys
import pygame
import pygame_gui as pgui
from enum import Enum

from settings import Settings
import tilemap
import sprite


class GameState(Enum):
    MENU = 0
    PLAYING = 1


class Hexer:
    """Class used to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create the game window"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height))

        self.manager = pgui.UIManager(
            (self.settings.screen_width, self.settings.screen_height), 'theme.json')

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Hexer")

        # Instantiate a tilemap, fill it with tiles, add tiles to group
        self.gameMap = tilemap.Map(self.settings.map_radius, self)
        self.tiles = self.gameMap.fill_map()

        # Instantiate player and add him to player_group
        self.player = sprite.Player(0, 0, 0)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.initialize_UI()

    def initialize_UI(self):
        """Initializes all starting UI elements"""
        self.quit_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 10), (90, 40)), text='Quit', manager=self.manager)
        self.turn_advance_button = pgui.elements.UIButton(relative_rect=pygame.Rect(
            (10, 60), (90, 40)), text='Advance turn', manager=self.manager)
        self.healthbar = pgui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((890, 10), (300, 40)), manager=self.manager, sprite_to_monitor=self.player)

    def run_game(self):
        """Start the main game loop"""

        while True:

            time_delta = self.clock.tick(60) / 1000.0
            self.manager.update(time_delta)

            # Check for keyboard / mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        sys.exit()
                    if event.ui_element == self.turn_advance_button:
                        print("ADVANCE!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.move(event.pos[0], event.pos[1])
                    if event.button == 3:
                        self.gameMap.curseTile(event.pos[0], event.pos[1])

                self.manager.process_events(event)

            self.gameMap.highlightTile(pygame.mouse.get_pos()[
                                       0], pygame.mouse.get_pos()[1])
            self.gameMap.update()

            # Redraw screen background every frame
            self.redraw_screen()

            # Refresh the display
            self.clock.tick(60)
            pygame.display.flip()

    def redraw_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.manager.draw_ui(self.screen)
        self.tiles.draw(self.screen)
        self.player_group.draw(self.screen)
