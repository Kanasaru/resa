""" This module provides the starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import logging
from datetime import datetime
from data.editor import Editor
from data.handlers.sound import SoundHandler
from data.settings import conf
import data.eventcodes as ecodes
from data.game import Game
from data.interfaces.mainmenu import MainMenu
from data.interfaces.options import Options
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.handlers.music import Music
from data.handlers.locals import LocalsHandler
from data.handlers.msg import Message


class Start(object):
    def __init__(self) -> None:
        """ Initializes the titles """
        pygame.init()

        # event handling varibales
        self.start_game = False
        self.load_game = False
        self.leave_game = False
        self.options = False
        self.start_editor = False
        self.editor = None

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # build window
        resos = Options.get_screenmodes()
        conf.resolution = resos['win'][-1]
        self.surface = pygame.display.set_mode(conf.resolution)
        pygame.display.set_icon(pygame.image.load(conf.icon).convert())
        pygame.display.set_caption(f"{LocalsHandler.lang('info_welcome')} {conf.title}")
        self.resolution_buffer = conf.resolution

        # create titles
        hdl_sp_main_menu = SpriteSheetHandler()
        buttons = SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size)
        buttons.colorkey = (1, 0, 0)
        hdl_sp_main_menu.add(buttons)
        switches = SpriteSheet(conf.sp_menu_swt_key, conf.sp_menu_swt, conf.sp_menu_swt_size)
        switches.colorkey = (1, 0, 0)
        hdl_sp_main_menu.add(switches)
        self.title_main = MainMenu(hdl_sp_main_menu, conf.sp_menu_btn_key)
        self.title_options = Options(hdl_sp_main_menu)

        # messages
        self.messages = Message(hdl_sp_main_menu, conf.sp_menu_btn_key)

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
                    conf.resolution = event.res
                    self.update_display()
                elif event.code == ecodes.RESA_BTN_EDITOR:
                    self.start_editor = True
                elif event.code == ecodes.RESA_SWT_FULLSCREEN:
                    conf.fullscreen = event.fullscreen
                    conf.resolution = event.res
                    self.update_display()
            elif event.type == ecodes.RESA_MUSIC_ENDED_EVENT:
                if len(self.music.playlist) > 0:
                    self.music.load_next()
                else:
                    self.music.refill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_p:
                    self.music.pause()
                elif event.key == pygame.K_PLUS:
                    self.music.volume += .1
                elif event.key == pygame.K_MINUS:
                    self.music.volume -= .1

            self.messages.handle_event(event)
            if self.options:
                self.title_options.handle_event(event)
            else:
                self.title_main.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if self.start_editor:
            # editor was closed and back to main menu
            if self.editor is not None:
                # restore display settings
                conf.resolution = self.resolution_buffer[0]
                conf.fullscreen = self.resolution_buffer[1]
                pygame.display.set_caption(f"{LocalsHandler.lang('info_welcome')} {conf.title}")
                self.update_display()
                self.start_editor = False
                self.editor = None
            else:
                # store current display settings, create new display and start editor
                self.resolution_buffer = (conf.resolution, conf.fullscreen)
                conf.resolution = (1280, 960)
                conf.fullscreen = False
                pygame.display.set_caption(f"{LocalsHandler.lang('info_editor_title')} {conf.title}")
                self.update_display()
                self.editor = Editor()
        elif self.start_game:
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

            self.title_options.run_logic()
        else:
            self.title_main.run_logic()

        self.messages.run_logic()

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

        # render message and info boxes
        self.messages.render(self.surface)

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
        filename = f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{LocalsHandler.lang('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def update_display(self):
        """ Reloads the display and re-builds the interfaces.

        :return: None
        """
        if conf.fullscreen:
            self.surface = pygame.display.set_mode(conf.resolution, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(conf.resolution)

        # re-build interfaces
        self.title_main.rect = pygame.Rect((0, 0), conf.resolution)
        self.title_main.build()
        self.title_options.rect = pygame.Rect((0, 0), conf.resolution)
        self.title_options.build()
