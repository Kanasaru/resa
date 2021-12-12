""" This module provides starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
from data.settings import conf
import data.eventcodes as ecodes
from data.game import Game
from data.interfaces.mainmenu import MainMenu
from data.interfaces.options import Options
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.handlers.music import Music


class Start(object):

    def __init__(self) -> None:
        """ Initializes the game """
        pygame.init()

        self.start_game = False
        self.load_game = False
        self.leave_game = False
        self.options = False
        self.resolution_update = None
        self.game = None
        self.music = Music()
        self.clock = pygame.time.Clock()
        # self.desktop_resolutions = pygame.display.get_desktop_sizes()
        # self.full_screen_resolutions = pygame.display.list_modes()
        self.surface = pygame.display.set_mode(conf.resolution)
        pygame.display.set_icon(pygame.image.load('resources/images/icon.png').convert())
        pygame.display.set_caption(f"{conf.title}")

        hdl_sp_main_menu = SpriteSheetHandler()
        buttons = SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size)
        buttons.colorkey = (1, 0, 0)
        hdl_sp_main_menu.add(buttons)
        self.title_main = MainMenu(hdl_sp_main_menu, conf.sp_menu_btn_key)
        self.title_options = Options(hdl_sp_main_menu, conf.sp_menu_btn_key)

        self.music.load()
        self.loop()

    def loop(self) -> None:
        """ game loop

        :return: None
        """
        self.music.start(conf.volume)
        while not self.leave_game:
            self.clock.tick(conf.fps)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self) -> None:
        """ Handles all events

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game = True
            elif event.type == ecodes.RESA_TITLE_EVENT:
                if event.code == ecodes.RESA_STARTGAME:
                    self.start_game = True
                elif event.code == ecodes.RESA_LOADGAME:
                    self.start_game = True
                    self.load_game = True
                elif event.code == ecodes.RESA_OPTIONS:
                    self.options = True
                elif event.code == ecodes.RESA_QUITGAME:
                    self.leave_game = True
                elif event.code == ecodes.RESA_MAINMENU:
                    self.options = False
                elif event.code == ecodes.RESA_CHG_RESOLUTION:
                    self.resolution_update = event.res
                else:
                    pass
            elif event.type == ecodes.RESA_MUSIC_ENDED_EVENT:
                if len(self.music.playlist) > 0:
                    self.music.load_next()
                else:
                    self.music.refill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.music.pause()
                if event.key == pygame.K_PLUS:
                    self.music.volume += .1
                if event.key == pygame.K_MINUS:
                    self.music.volume -= .1
            else:
                pass
            if self.options:
                self.title_options.handle_event(event)
            else:
                self.title_main.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if self.start_game:
            if self.game is not None and self.game.exit_game:
                self.music.load()
                self.music.start(conf.volume)
                self.start_game = False
                self.load_game = False
                self.game = None
            else:
                self.music.stop()
                self.game = Game(self.surface, self.load_game)
        if self.options:
            if self.resolution_update is not None:
                conf.resolution = self.resolution_update
                pygame.display.set_mode(conf.resolution)
                self.title_main.rect = pygame.Rect((0, 0), conf.resolution)
                self.title_main.build()
                self.title_options.rect = pygame.Rect((0, 0), conf.resolution)
                self.title_options.build()
                self.resolution_update = None
            self.title_options.run_logic()
        else:
            self.title_main.run_logic()

    def render(self) -> None:
        """ Renders everything to the display

        :return: None
        """
        self.surface.fill(conf.COLOR_WHITE)
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
