""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import datetime
import data.helpers.color as colors
import pygame
import data.eventcodes as ecodes
from data.interfaces.debugscreen import DebugScreen
from data.interfaces.loadscreen import GameLoadScreen
from data.interfaces.gamepanel import GamePanel
from data.world.map import Loader
from data import settings
from data.handlers.debug import DebugHandler
from data.handlers.gamedata import GameDataHandler


class Game(object):
    def __init__(self, surface, load: bool = False):
        """ Initializes the in-game

        :param surface: surface the in-game should be rendered on
        """
        self.exit_game = False
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.map = None
        # handler
        self.debug_handler = DebugHandler()
        self.game_data_handler = GameDataHandler()
        self.game_data_handler.game_time_speed = settings.INGAME_SPEED
        # titles / screens
        self.debug_screen = DebugScreen()
        self.debug_screen.add('Version', lambda: settings.GAME_VERSION)
        self.debug_screen.add('Date', lambda: datetime.datetime.now().strftime("%A, %d. %B %Y"))
        self.debug_screen.add('In-Game time', self.game_data_handler.get_game_time)
        self.game_panel = GamePanel()
        # loading pre-data
        self.load_msg()
        self.load_map(load)
        # start game loop
        self.loop()

    def load_map(self, load: bool):
        self.map = Loader((settings.RESOLUTION[0] - 2, settings.RESOLUTION[1] - self.game_panel.rect.height - 2),
                          (40, 20))
        if load:
            self.game_data_handler.read_from_file(settings.SAVE_FILE)
            self.map.build_world(self.game_data_handler.world_data)
        else:
            self.map.build_world()
        self.game_panel.resources = self.game_data_handler.resources

    def loop(self) -> None:
        """ in-game loop

        :return: None
        """
        while not self.exit_game:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self) -> None:
        """ Handles all in-game events

        :return: None
        """
        # game panel events
        for event in self.game_panel.get_events():
            if event.code == ecodes.STOPGAME:
                self.exit_game = True
            elif event.code == ecodes.SAVEGAME:
                self.game_data_handler.world_data = (self.map.get_rect(), self.map.get_raw_fields(), self.map.get_raw_treess())
                self.game_data_handler.save_to_file(settings.SAVE_FILE)
            else:
                pass
        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass
                    # z = pygame.mouse.get_pos()
                if event.button == 2:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F3:
                    self.debug_handler.toggle()
            else:
                pass
            # event handler
            self.debug_screen.handle_event(event)
            self.game_panel.handle_event(event)
            self.map.handle_event(event)
        # clear event queues
        self.debug_screen.clear_events()
        self.game_panel.clear_events()

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
        self.game_data_handler.update()
        # debugging
        self.debug_handler.update()
        self.debug_screen.timer = self.debug_handler.play_time
        self.debug_screen.run_logic()

        # game panel
        self.game_panel.run_logic()

        # map
        self.map.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        # basic
        self.surface.fill(colors.COLOR_WHITE)
        # map
        self.map.render()
        pygame.Surface.blit(self.surface, self.map.get_surface(), (1, self.game_panel.rect.height + 1))
        # game panel
        self.game_panel.render(self.surface)
        # debug screen
        if self.debug_handler:
            self.debug_screen.render(self.surface)

        pygame.display.flip()

    def load_msg(self) -> None:
        """ Creates and displays the world loading title

        :return: None
        """
        load_screen = GameLoadScreen()
        load_screen.render(self.surface)
        pygame.display.flip()
