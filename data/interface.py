""" This module provides title screens for the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.1'

import pygame
from data.forms.textbox import Textbox
from data.forms.button import Button
from data.forms.title import Title
from data.helpers.event import Event
import data.eventcodes as ecodes
from data import settings


class MainMenu(object):
    def __init__(self):
        self.name = "main"
        self.bg_image = settings.MENU_BG_IMG
        self.bg_color = settings.COLOR_BLACK
        self.rect = pygame.Rect((0, 0), settings.RESOLUTION)
        self.__credits = f"Created and Designed by {settings.GAME_AUTHOR} | {settings.GAME_WWW}"

        self.__build()

    def __build(self):
        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        # textboxes
        tf_headline = Textbox("tf_headline", (int(self.title.width() / 2), 20), settings.GAME_TITLE.upper(), 90)
        tf_headline.align(tf_headline.CENTER)
        tf_version = Textbox("tf_version", (self.title.width() - 5, 5), f"v{settings.GAME_VERSION}", 14)
        tf_version.align(tf_version.RIGHT)
        tf_credits = Textbox("tf_credits", (int(self.title.width() / 2), self.title.height() - 24), self.__credits, 14)
        tf_credits.align(tf_credits.CENTER)
        # buttons
        width, height = tf_headline.get_dimensions()
        position_y = height + 100
        b_newgame = Button(
            "b_newgame",
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
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
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Load Game",
            Event(ecodes.LOADGAME, ecodes.LOADGAME)
        )
        b_loadgame.align(b_loadgame.CENTER)
        try:
            f = open(settings.SAVE_FILE)
            f.close()
        except FileNotFoundError:
            b_loadgame.disable()
        b_loadgame.set_spritesheet(settings.SPRITES_MENU_BUTTONS, (220, 60))
        position_y += b_loadgame.height() + 20
        b_quitgame = Button(
            "b_quitgame",
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            settings.SPRITES_MENU_BUTTONS, (220, 60),
            "Quit Game",
            Event(ecodes.QUITGAME, ecodes.QUITGAME)
        )
        b_quitgame.align(b_quitgame.CENTER)
        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits])
        self.title.add([b_newgame, b_loadgame, b_quitgame])

    def get_events(self):
        return self.title.get_events()

    def handle_event(self, event):
        self.title.handle_event(event)

    def clear_events(self):
        self.title.clear_events()

    def run_logic(self):
        self.title.run_logic()

    def update(self):
        self.__build()

    def render(self, surface: pygame.Surface):
        self.title.render(surface)


class GameLoadScreen(object):
    def __init__(self):
        self.name = "load_screen"
        self.bg_image = None
        self.bg_color = settings.COLOR_BLACK
        self.rect = pygame.Rect((0, 0), settings.RESOLUTION)
        self.text = f"Loading world..."

        self.__build()

    def __build(self):
        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        # textboxes
        position = (int(self.title.width() / 2), int(self.title.height() / 2))
        tf_load_screen = Textbox("tf_load_screen", position, self.text, 20)
        tf_load_screen.font_color(settings.COLOR_WHITE)
        tf_load_screen.align(tf_load_screen.CENTER)
        # add form objects to title
        self.title.add(tf_load_screen)

    def get_events(self):
        return self.title.get_events()

    def handle_event(self, event):
        self.title.handle_event(event)

    def clear_events(self):
        self.title.clear_events()

    def run_logic(self):
        self.title.run_logic()

    def update(self):
        self.__build()

    def render(self, surface: pygame.Surface):
        self.title.render(surface)


class GamePanel(object):
    def __init__(self):
        self.name = "panel"
        self.bg_image = None
        self.bg_color = settings.COLOR_BLACK
        self.rect = pygame.Rect((0, 0), (settings.RESOLUTION[0], 30))
        self.resources = f"Wood: 0 | Stone: 0 | Marble: 0 | Tools: 0 | Gold: 0"

        self.__build()

    def __build(self):
        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        # textboxes
        tf_version = Textbox("tf_version", (5, 5), f"v{settings.GAME_VERSION}", 14)
        tf_version.font_color(settings.COLOR_WHITE)
        tf_version.align(tf_version.LEFT)
        tf_resources = Textbox("tf_resources",
                               (int(self.title.width() / 2), 5),
                               self.resources, 14, self.update_resources)
        tf_resources.font_color(settings.COLOR_WHITE)
        tf_resources.align(tf_resources.CENTER)
        # buttons
        b_quit = Button(
            "b_quit",
            pygame.Rect(self.title.width() - 5, 3, 70, 24),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Quit",
            Event(ecodes.STOPGAME, ecodes.STOPGAME)
        )
        b_quit.align(b_quit.RIGHT)
        b_quit.set_font(settings.BASIC_FONT, 13)
        b_save = Button(
            "b_save",
            pygame.Rect(self.title.width() - 80, 3, 70, 24),
            settings.SPRITES_MENU_BUTTONS,
            (220, 60),
            "Save",
            Event(ecodes.SAVEGAME, ecodes.SAVEGAME)
        )
        b_save.align(b_save.RIGHT)
        b_save.set_font(settings.BASIC_FONT, 13)
        # add form objects to title
        self.title.add([tf_resources, tf_version])
        self.title.add([b_save, b_quit])

    def get_events(self):
        return self.title.get_events()

    def handle_event(self, event):
        self.title.handle_event(event)

    def clear_events(self):
        self.title.clear_events()

    def run_logic(self):
        self.title.run_logic()

    def update_resources(self):
        return self.resources

    def render(self, surface: pygame.Surface):
        self.title.render(surface)
