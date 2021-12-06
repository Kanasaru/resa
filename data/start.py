""" This module provides starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
import data.eventcodes as ecodes
import data.helpers.color as colors
from data.game import Game
from data.interfaces.mainmenu import MainMenu
from data.interfaces.options import Options
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.music import Music
from data import settings


class Start(object):
    def __init__(self) -> None:
        """ Initializes the game """
        pygame.init()

        self.start_game = False
        self.load_game = False
        self.leave_game = False
        self.music = Music()

        self.game = None
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(settings.RESOLUTION)

        pygame.display.set_caption(f"{settings.GAME_TITLE}")

        main_menu_sheet_handler = SpriteSheetHandler()
        buttons = SpriteSheet(
            settings.SPRITES_MENU_BUTTONS_KEY,
            settings.SPRITES_MENU_BUTTONS,
            settings.SPRITES_MENU_BUTTONS_SIZE
        )
        buttons.colorkey = (1, 0, 0)
        main_menu_sheet_handler.add(buttons)
        self.title_main = MainMenu(main_menu_sheet_handler, settings.SPRITES_MENU_BUTTONS_KEY)
        self.title_options = Options(main_menu_sheet_handler, settings.SPRITES_MENU_BUTTONS_KEY)
        self.options = False
        self.resolution_update = None

        self.music.load_music()
        self.loop()

    def loop(self) -> None:
        """ game loop

        :return: None
        """
        self.music.start_music()
        while not self.leave_game:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self) -> None:
        """ Handles all events

        :return: None
        """
        for event in self.title_main.get_events():
            if event.code == ecodes.STARTGAME:
                self.start_game = True
            elif event.code == ecodes.LOADGAME:
                self.start_game = True
                self.load_game = True
            elif event.code == ecodes.OPTIONS:
                self.options = True
            elif event.code == ecodes.QUITGAME:
                self.leave_game = True
            else:
                pass

        for event in self.title_options.get_events():
            if event.code == ecodes.MAINMENU:
                self.options = False
            elif event.code == ecodes.RES_1920:
                self.resolution_update = (1920, 1080)
            elif event.code == ecodes.RES_1000:
                self.resolution_update = (1000, 600)
            elif event.code == ecodes.RES_800:
                self.resolution_update = (800, 600)
            else:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.music.pause_music()
                if event.key == pygame.K_PLUS:
                    self.music.change_volume(self.music.volume + 0.1)
                if event.key == pygame.K_MINUS:
                    self.music.change_volume(self.music.volume - 0.1)
            else:
                pass
            if self.options:
                self.title_options.handle_event(event)
            else:
                self.title_main.handle_event(event)

        self.title_main.clear_events()
        self.title_options.clear_events()

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if self.start_game:
            if self.game is not None and self.game.exit_game:
                self.music.load_music()
                self.music.start_music()
                self.start_game = False
                self.load_game = False
                self.game = None
            else:
                self.clr_screen()
                self.music.stop_music()
                self.game = Game(self.surface, self.load_game)
        if self.options:
            if self.resolution_update is not None:
                settings.RESOLUTION = self.resolution_update
                pygame.display.set_mode(settings.RESOLUTION)
                self.title_main.rect = pygame.Rect((0, 0), settings.RESOLUTION)
                self.title_main.build()
                self.title_options.rect = pygame.Rect((0, 0), settings.RESOLUTION)
                self.title_options.build()
                self.resolution_update = None
            self.title_options.run_logic()
        else:
            self.title_main.run_logic()

    def render(self) -> None:
        """ Renders everything to the display

        :return: None
        """
        self.surface.fill(colors.COLOR_WHITE)
        if self.options:
            self.title_options.render(self.surface)
        else:
            self.title_main.render(self.surface)
        pygame.display.flip()

    def exit(self):
        """ Exit routine of the game

        :return: None
        """
        pygame.quit()
        print("Bye bye!")

    def clr_screen(self) -> None:
        """ Clears the display of the game

        :return: None
        """
        self.surface.fill(colors.COLOR_BLACK)
        pygame.display.flip()
