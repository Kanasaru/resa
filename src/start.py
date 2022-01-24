""" This module provides the starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import logging
from datetime import datetime
import src.locales as locales
from src.handler import RESA_CH, RESA_GSH, RESA_SH, RESA_MH, RESA_EH
import src.ui.display
from src.ui.editor import Editor
from src.ui.form import MessageHandler
from src.ui.titles import MainMenu, Options
from src.game import Game


class Start(object):
    def __init__(self) -> None:
        """ Initializes the titles """

        # event handling varibales
        self.editor = None

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # build window
        resos = src.ui.display.get_screenmodes()
        self.surface = pygame.display.set_mode(resos['win'][-1])
        pygame.display.set_icon(pygame.image.load(RESA_CH.icon).convert())
        pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")
        self.resolution_buffer = pygame.display.get_surface().get_size()
        self.resolution = pygame.display.get_surface().get_size()

        # create titles
        self.title_main = MainMenu('MenuButtons')
        self.title_options = Options('MenuButtons')

        # messages
        self.messages = MessageHandler('MenuButtons')

        # start the game loop
        self.game = None
        self.loop()

    def loop(self) -> None:
        """ Game loop

        :return: None
        """
        RESA_MH.start(RESA_CH.volume)

        while not RESA_GSH.leave_game:
            self.clock.tick(RESA_CH.fps)
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
                RESA_GSH.leave_game = True
            elif event.type == RESA_EH.RESA_TITLE_EVENT:
                if event.code == RESA_EH.RESA_BTN_STARTGAME:
                    RESA_GSH.start_game = True
                elif event.code == RESA_EH.RESA_BTN_LOADGAME:
                    RESA_GSH.start_game = True
                    RESA_GSH.load_game = True
                elif event.code == RESA_EH.RESA_BTN_OPTIONS:
                    RESA_GSH.options = True
                elif event.code == RESA_EH.RESA_BTN_QUITGAME:
                    RESA_GSH.leave_game = True
                elif event.code == RESA_EH.RESA_BTN_MAINMENU:
                    RESA_GSH.options = False
                elif event.code == RESA_EH.RESA_BTN_CHG_RESOLUTION:
                    self.resolution = event.res
                    self.update_display()
                elif event.code == RESA_EH.RESA_BTN_EDITOR:
                    RESA_GSH.start_editor = True
                elif event.code == RESA_EH.RESA_SWT_FULLSCREEN:
                    RESA_CH.fullscreen = event.fullscreen
                    self.resolution = event.res
                    self.update_display()
            elif event.type == RESA_EH.RESA_MUSIC_ENDED_EVENT:
                if len(RESA_MH.playlist) > 0:
                    RESA_MH.load_next()
                else:
                    RESA_MH.refill()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_p:
                    RESA_MH.pause()
                elif event.key == pygame.K_PLUS:
                    RESA_MH.volume += .1
                elif event.key == pygame.K_MINUS:
                    RESA_MH.volume -= .1

            self.messages.handle_event(event)
            if RESA_GSH.options:
                self.title_options.handle_event(event)
            else:
                self.title_main.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if RESA_GSH.start_editor:
            # editor was closed and back to main menu
            if self.editor is not None:
                # restore display settings
                self.resolution = self.resolution_buffer[0]
                RESA_CH.fullscreen = self.resolution_buffer[1]
                pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")
                self.update_display()
                RESA_GSH.start_editor = False
                self.editor = None
            else:
                # store current display settings, create new display and start editor
                self.resolution_buffer = (pygame.display.get_surface().get_size(), RESA_CH.fullscreen)
                self.resolution = (1280, 960)
                RESA_CH.fullscreen = False
                pygame.display.set_caption(f"{locales.get('info_editor_title')} {RESA_CH.title}")
                self.update_display()
                self.editor = Editor()
        elif RESA_GSH.start_game:
            # current game play ended and back to main menu
            if self.game is not None and RESA_GSH.exit_game:
                RESA_MH.load()
                RESA_MH.start(RESA_CH.volume)
                RESA_GSH.start_game = False
                RESA_GSH.load_game = False
                self.game = None
            # start a game
            else:
                RESA_MH.stop()
                self.game = Game(RESA_GSH.load_game)

            self.title_options.run_logic()
        else:
            self.title_main.run_logic()

        self.messages.run_logic()

    def render(self) -> None:
        """ Renders everything to the display

        :return: None
        """
        self.surface.fill(RESA_CH.COLOR_WHITE)

        # render current title
        if RESA_GSH.options:
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
        RESA_SH.play('screenshot')
        filename = f'{RESA_CH.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{locales.get('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def update_display(self):
        """ Reloads the display and re-builds the interfaces.

        :return: None
        """
        if RESA_CH.fullscreen:
            self.surface = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(self.resolution)

        # re-build interfaces
        self.title_main.rect = pygame.Rect((0, 0), self.resolution)
        self.title_main.build()
        self.title_options.rect = pygame.Rect((0, 0), self.resolution)
        self.title_options.build()
