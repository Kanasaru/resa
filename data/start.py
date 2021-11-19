""" This module provides starting routine for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'

import pygame
import data.eventcodes as ecodes
from data.helpers.event import Event
from data.game import Game
from data.forms.textbox import Textbox
from data.forms.button import Button
from data.forms.title import Title
from data import settings


class Start(object):
    def __init__(self) -> None:
        """ Initializes the game """
        pygame.init()

        self.start_game = False
        self.leave_game = False
        self.pause = False

        self.game = None
        self.title_main = None
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(settings.RESOLUTION)

        pygame.display.set_caption(f"{settings.GAME_TITLE}")

        self.load_music()
        self.build_titles()
        self.loop()

    def loop(self) -> None:
        """ game loop

        :return: None
        """
        self.start_music(settings.MUSIC_VOLUME, settings.MUSIC_LOOP)
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
                print("Load Game!")
            elif event.code == ecodes.QUITGAME:
                self.leave_game = True
            else:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pause_music()
            else:
                pass
            self.title_main.handle_event(event)

        self.title_main.clear_events()

    def run_logic(self) -> None:
        """ Runs the game logic

        :return: None
        """
        if self.start_game:
            if self.game is not None and self.game.exit_game:
                self.load_music()
                self.start_music(settings.MUSIC_VOLUME, settings.MUSIC_LOOP)
                self.start_game = False
                self.game = None
            else:
                self.clr_screen()
                self.stop_music()
                self.game = Game(self.surface)

        self.title_main.run_logic()

    def render(self) -> None:
        """ Renders everything to the display

        :return: None
        """
        self.surface.fill(settings.COLOR_WHITE)
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
        self.surface.fill(settings.COLOR_BLACK)
        pygame.display.flip()

    def load_music(self) -> None:
        """ Loads the background music into the mixer

        :return: None
        """
        pygame.mixer.music.load(settings.MUSIC_BG_1)

    def start_music(self, volume: float, loop: int) -> None:
        """ Starts the background music

        :param volume: volume the music starts at
        :param loop: if true the music plays infinitely
        :return: None
        """
        pygame.mixer.music.play(loop)
        pygame.mixer.music.set_volume(volume)

    def pause_music(self) -> None:
        """ Toggles background music on and off

        :return: None
        """
        if self.pause:
            pygame.mixer.music.unpause()
            self.pause = False
        else:
            pygame.mixer.music.pause()
            self.pause = True

    def stop_music(self) -> None:
        """ Stops the background music

        :return: None
        """
        pygame.mixer.music.stop()

    def build_titles(self) -> None:
        """ Creates the main title of the game

        :return: None
        """
        self.title_main = Title(
            "main",
            pygame.Rect(0, 0, settings.RESOLUTION[0], settings.RESOLUTION[1]),
            settings.COLOR_BLACK,
            settings.MENU_BG_IMG
        )
        tf_headline = Textbox(
            "tf_headline",
            (int(self.title_main.width() / 2), 20),
            "RESA",
            90
        )
        tf_headline.align(tf_headline.CENTER)
        tf_version = Textbox(
            "tf_version",
            (self.title_main.width() - 5, 5),
            f"Version: {settings.GAME_VERSION}",
            14
        )
        tf_version.align(tf_version.RIGHT)
        tf_credits = Textbox(
            "tf_credits",
            (int(self.title_main.width() / 2), self.title_main.height() - 24),
            f"Created and Designed by {settings.GAME_AUTHOR} | {settings.GAME_WWW}",
            14
        )
        tf_credits.align(tf_credits.CENTER)
        width, height = tf_headline.get_dimensions()
        position_y = height + 100
        b_newgame = Button(
            "b_newgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "New Game",
            Event(ecodes.STARTGAME, ecodes.STARTGAME)
        )
        b_newgame.align(b_newgame.CENTER)
        b_newgame.set_spritesheet(settings.SPRITES_MENU_BUTTONS, (220, 60))
        position_y += b_newgame.height() + 20
        b_loadgame = Button(
            "b_loadgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Load Game",
            Event(ecodes.LOADGAME, ecodes.LOADGAME)
        )
        b_loadgame.align(b_loadgame.CENTER)
        b_loadgame.disable()
        b_loadgame.set_spritesheet(settings.SPRITES_MENU_BUTTONS, (220, 60))
        position_y += b_loadgame.height() + 20
        b_quitgame = Button(
            "b_quitgame",
            pygame.Rect(self.title_main.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS, (220, 60),
            "Quit Game",
            Event(ecodes.QUITGAME, ecodes.QUITGAME)
        )
        b_quitgame.align(b_quitgame.CENTER)

        self.title_main.add(tf_headline)
        self.title_main.add(tf_version)
        self.title_main.add(tf_credits)
        self.title_main.add(b_newgame)
        self.title_main.add(b_loadgame)
        self.title_main.add(b_quitgame)
