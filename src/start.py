""" This module provides the starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import logging
from datetime import datetime
import src.locales as locales
import src.handler
import src.ui.display
from src.ui.editor import Editor
from src.ui.form import MessageHandler
from src.ui.titles import MainMenu, Options
from src.handler import conf
from src.game import Game


class Start(object):
    def __init__(self) -> None:
        """ Initializes the titles """

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
        resos = src.ui.display.get_screenmodes()
        self.surface = pygame.display.set_mode(resos['win'][-1])
        pygame.display.set_icon(pygame.image.load(conf.icon).convert())
        pygame.display.set_caption(f"{locales.get('info_welcome')} {conf.title}")
        self.resolution_buffer = pygame.display.get_surface().get_size()
        self.resolution = pygame.display.get_surface().get_size()

        # create titles
        self.title_main = MainMenu(src.handler.hdl_sh_titles, conf.sp_menu_btn_key)
        self.title_options = Options(src.handler.hdl_sh_titles, conf.sp_menu_btn_key)

        # messages
        self.messages = MessageHandler(src.handler.hdl_sh_titles, conf.sp_menu_btn_key)

        # start the game loop
        self.game = None
        self.loop()

    def loop(self) -> None:
        """ Game loop

        :return: None
        """
        src.handler.hdl_music.start(conf.volume)

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
            elif event.type == src.handler.RESA_TITLE_EVENT:
                if event.code == src.handler.RESA_BTN_STARTGAME:
                    self.start_game = True
                elif event.code == src.handler.RESA_BTN_LOADGAME:
                    self.start_game = True
                    self.load_game = True
                elif event.code == src.handler.RESA_BTN_OPTIONS:
                    self.options = True
                elif event.code == src.handler.RESA_BTN_QUITGAME:
                    self.leave_game = True
                elif event.code == src.handler.RESA_BTN_MAINMENU:
                    self.options = False
                elif event.code == src.handler.RESA_BTN_CHG_RESOLUTION:
                    self.resolution = event.res
                    self.update_display()
                elif event.code == src.handler.RESA_BTN_EDITOR:
                    self.start_editor = True
                elif event.code == src.handler.RESA_SWT_FULLSCREEN:
                    conf.fullscreen = event.fullscreen
                    self.resolution = event.res
                    self.update_display()
            elif event.type == src.handler.RESA_MUSIC_ENDED_EVENT:
                if len(src.handler.hdl_music.playlist) > 0:
                    src.handler.hdl_music.load_next()
                else:
                    src.handler.hdl_music.refill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_p:
                    src.handler.hdl_music.pause()
                elif event.key == pygame.K_PLUS:
                    src.handler.hdl_music.volume += .1
                elif event.key == pygame.K_MINUS:
                    src.handler.hdl_music.volume -= .1

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
                self.resolution = self.resolution_buffer[0]
                conf.fullscreen = self.resolution_buffer[1]
                pygame.display.set_caption(f"{locales.get('info_welcome')} {conf.title}")
                self.update_display()
                self.start_editor = False
                self.editor = None
            else:
                # store current display settings, create new display and start editor
                self.resolution_buffer = (pygame.display.get_surface().get_size(), conf.fullscreen)
                self.resolution = (1280, 960)
                conf.fullscreen = False
                pygame.display.set_caption(f"{locales.get('info_editor_title')} {conf.title}")
                self.update_display()
                self.editor = Editor()
        elif self.start_game:
            # current game play ended and back to main menu
            if self.game is not None and self.game.exit_game:
                src.handler.hdl_music.load()
                src.handler.hdl_music.start(conf.volume)
                self.start_game = False
                self.load_game = False
                self.game = None
            # start a game
            else:
                src.handler.hdl_music.stop()
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
        src.handler.hdl_sound.play('screenshot')
        filename = f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{locales.get('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def update_display(self):
        """ Reloads the display and re-builds the interfaces.

        :return: None
        """
        if conf.fullscreen:
            self.surface = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(self.resolution)

        # re-build interfaces
        self.title_main.rect = pygame.Rect((0, 0), self.resolution)
        self.title_main.build()
        self.title_options.rect = pygame.Rect((0, 0), self.resolution)
        self.title_options.build()
