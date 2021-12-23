""" This module provides the starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
import logging
from datetime import datetime
from data.handlers.sound import SoundHandler
from data.settings import conf
import data.eventcodes as ecodes
from data.game import Game
from data.interfaces.mainmenu import MainMenu
from data.interfaces.options import Options
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.handlers.music import Music


class Start(object):
    def __init__(self) -> None:
        """ Initializes the titles """
        pygame.init()

        # event handling varibales
        self.start_game = False
        self.load_game = False
        self.leave_game = False
        self.options = False
        self.resolution_update = None
        self.screenshot = False

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # build window
        self.surface = pygame.display.set_mode(conf.resolution)
        pygame.display.set_icon(pygame.image.load(conf.icon).convert())
        pygame.display.set_caption(f'Welcome to {conf.title}')

        # create titles
        hdl_sp_main_menu = SpriteSheetHandler()
        buttons = SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size)
        buttons.colorkey = (1, 0, 0)
        hdl_sp_main_menu.add(buttons)
        self.title_main = MainMenu(hdl_sp_main_menu, conf.sp_menu_btn_key)
        self.title_options = Options(hdl_sp_main_menu, conf.sp_menu_btn_key)

        # load sounds and music
        self.music = Music()
        self.music.load()
        self.sounds = SoundHandler()

        # start the game loop
        self.game = None
        self.loop()

    def loop(self) -> None:
        """ Game loop

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
                if event.code == ecodes.RESA_BTN_STARTGAME:
                    self.start_game = True
                elif event.code == ecodes.RESA_BTN_LOADGAME:
                    self.start_game = True
                    self.load_game = True
                elif event.code == ecodes.RESA_BTN_OPTIONS:
                    self.options = True
                elif event.code == ecodes.RESA_BTN_QUITGAME:
                    self.leave_game = True
                elif event.code == ecodes.RESA_BTN_MAINMENU:
                    self.options = False
                elif event.code == ecodes.RESA_BTN_CHG_RESOLUTION:
                    self.resolution_update = event.res
                else:
                    pass
            elif event.type == ecodes.RESA_MUSIC_ENDED_EVENT:
                if len(self.music.playlist) > 0:
                    self.music.load_next()
                else:
                    self.music.refill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.screenshot = True
                if event.key == pygame.K_p:
                    self.music.pause()
                if event.key == pygame.K_PLUS:
                    self.music.volume += .1
                if event.key == pygame.K_MINUS:
                    self.music.volume -= .1
            else:
                pass

            # push event into current title event handling
            if self.options:
                self.title_options.handle_event(event)
            else:
                self.title_main.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if self.start_game:
            # current game play ended and back to main menu
            if self.game is not None and self.game.exit_game:
                self.music.load()
                self.music.start(conf.volume)
                self.start_game = False
                self.load_game = False
                self.game = None
            # start a game
            else:
                self.music.stop()
                self.game = Game(self.load_game)
        if self.options:
            # change resolution and rebuild titles
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

        # screenshot
        if self.screenshot:
            self.take_screenshot()

    def render(self) -> None:
        """ Renders everything to the display

        :return: None
        """
        self.surface.fill(conf.COLOR_WHITE)

        # render current title
        if self.options:
            self.title_options.render(self.surface)
        else:
            self.title_main.render(self.surface)

        # display surface
        pygame.display.flip()

    @staticmethod
    def exit():
        """ Exit routine of the game

        :return: None
        """
        pygame.quit()
        print("Bye bye!")

    def take_screenshot(self) -> None:
        """ Saves the current screen as an image.

        :return: None
        """
        self.sounds.play('screenshot')
        pygame.image.save(pygame.display.get_surface(),
                          f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
        logging.info('Took screenshot')
        self.screenshot = False
