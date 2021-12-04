""" This module provides the MainMenu class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button
from data.helpers.event import Event
import data.eventcodes as ecodes
import data.helpers.color as colors
from data import settings


class MainMenu(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.name = 'main'
        self.rect = pygame.Rect((0, 0), settings.RESOLUTION)
        self.bg_color = colors.COLOR_BLACK
        self.bg_image = settings.MENU_BG_IMG
        self.__credits = f'Created and Designed by {settings.GAME_AUTHOR} | {settings.GAME_WWW}'

        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)

        # labels
        tf_headline = Label('tf_headline', (int(self.title.width() / 2), 20), settings.GAME_TITLE.upper())
        tf_headline.set_font(settings.BASIC_FONT, 90)
        tf_headline.align(tf_headline.CENTER)
        tf_version = Label('tf_version', (self.title.width() - 5, 5), f'v{settings.GAME_VERSION}')
        tf_version.set_font(settings.BASIC_FONT, 14)
        tf_version.align(tf_version.RIGHT)
        tf_credits = Label('tf_credits', (int(self.title.width() / 2), self.title.height() - 24), self.__credits)
        tf_credits.set_font(settings.BASIC_FONT, 14)
        tf_credits.align(tf_credits.CENTER)
        # buttons
        width, height = tf_headline.get_dimensions()
        position_y = height + 100
        b_newgame = Button(
            'b_newgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'New Game',
            Event(ecodes.STARTGAME, ecodes.STARTGAME)
        )
        b_newgame.set_font(settings.BASIC_FONT)
        b_newgame.align(b_newgame.CENTER)
        position_y += b_newgame.height() + 20
        b_loadgame = Button(
            'b_loadgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Load Game',
            Event(ecodes.LOADGAME, ecodes.LOADGAME)
        )
        b_loadgame.set_font(settings.BASIC_FONT)
        b_loadgame.align(b_loadgame.CENTER)
        try:
            f = open(settings.SAVE_FILE)
            f.close()
        except FileNotFoundError:
            b_loadgame.disable()
        position_y += b_loadgame.height() + 20
        b_quitgame = Button(
            'b_quitgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Quit Game',
            Event(ecodes.QUITGAME, ecodes.QUITGAME)
        )
        b_quitgame.set_font(settings.BASIC_FONT)
        b_quitgame.align(b_quitgame.CENTER)
        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits])
        self.title.add([b_newgame, b_loadgame, b_quitgame])