""" This module provides starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
from data.settings import conf
import data.eventcodes as ecodes
import data.helpers.color as colors
from data.game import Game
from data.interfaces.mainmenu import MainMenu
from data.interfaces.options import Options
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.music import Music


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
        # title events
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
                    self.music.pause()
                if event.key == pygame.K_PLUS:
                    self.music.volume += .1
                if event.key == pygame.K_MINUS:
                    self.music.volume -= .1
            elif event.type == pygame.USEREVENT:
                if len(self.music.playlist) > 0:
                    pygame.mixer.music.queue(self.music.playlist.pop())
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
                self.music.load()
                self.music.start()
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
