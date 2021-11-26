""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '0.2'

import pygame
import data.eventcodes as ecodes
from data.interface import GameLoadScreen, GamePanel
from data.world.map import Loader
from data import settings

from data.handler import GameDataHandler


class Game(object):
    def __init__(self, surface, load: bool = False):
        """ Initializes the in-game

        :param surface: surface the in-game should be rendered on
        """
        self.exit_game = False
        self.clock = pygame.time.Clock()
        self.surface = surface

        self.surface.fill(settings.COLOR_WHITE)
        self.game_panel = GamePanel()
        self.load_msg()

        self.map = Loader((settings.RESOLUTION[0] - 2, settings.RESOLUTION[1] - self.game_panel.rect.height - 2),
                          (40, 20))
        self.handler = GameDataHandler()
        if load:
            self.handler.read_from_file(settings.SAVE_FILE)
            self.map.build_world(self.handler.world_data)
        else:
            self.map.build_world()
        self.game_panel.resources = self.handler.resources

        self.loop()

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
        for event in self.game_panel.get_events():
            if event.code == ecodes.STOPGAME:
                self.exit_game = True
            elif event.code == ecodes.SAVEGAME:
                self.handler.world_data = (self.map.get_rect(), self.map.get_raw_fields())
                self.handler.save_to_file(settings.SAVE_FILE)
            else:
                pass

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
                    pass
            else:
                pass
            self.game_panel.handle_event(event)
            self.map.handle_event(event)

        self.game_panel.clear_events()

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
        self.game_panel.run_logic()
        self.map.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        self.surface.fill(settings.COLOR_WHITE)
        self.map.render()
        pygame.Surface.blit(self.surface, self.map.get_surface(), (1, self.game_panel.rect.height + 1))
        self.game_panel.render(self.surface)
        pygame.display.flip()

    def load_msg(self) -> None:
        """ Creates and displays the world loading title

        :return: None
        """
        load_screen = GameLoadScreen()
        load_screen.render(self.surface)
        pygame.display.flip()
