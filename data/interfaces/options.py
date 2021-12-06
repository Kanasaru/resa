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


class Options(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.name = 'options'
        self.rect = pygame.Rect((0, 0), settings.RESOLUTION)
        self.bg_color = colors.COLOR_BLACK
        self.bg_image = settings.MENU_BG_IMG
        self.__credits = f'Created and Designed by {settings.GAME_AUTHOR} | {settings.GAME_WWW}'

        self.build()

    def build(self):
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
        width, height = tf_headline.get_dimensions()
        position_y = height + 20
        tf_resolution = Label('tf_resolution', (int(self.title.width() / 2), position_y), 'Resolution')
        tf_resolution.set_font(settings.BASIC_FONT, 40)
        tf_resolution.align(tf_resolution.CENTER)
        # buttons
        position_y += tf_resolution.height() + 20
        b_1920x1080 = Button(
            'b_1920x1080',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '1920x1080',
            Event(ecodes.RES_1920, ecodes.RES_1920)
        )
        b_1920x1080.set_font(settings.BASIC_FONT)
        b_1920x1080.align(b_1920x1080.CENTER)
        position_y += b_1920x1080.height() + 20
        b_1000x600 = Button(
            'b_1000x600',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '1000x600',
            Event(ecodes.RES_1000, ecodes.RES_1000)
        )
        b_1000x600.set_font(settings.BASIC_FONT)
        b_1000x600.align(b_1000x600.CENTER)
        position_y += b_1000x600.height() + 20
        b_800x600 = Button(
            'b_800x600',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '800x600',
            Event(ecodes.RES_800, ecodes.RES_800)
        )
        b_800x600.set_font(settings.BASIC_FONT)
        b_800x600.align(b_800x600.CENTER)
        position_y += b_800x600.height() + 20
        b_back = Button(
            'b_back',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Back',
            Event(ecodes.MAINMENU, ecodes.MAINMENU)
        )
        b_back.set_font(settings.BASIC_FONT)
        b_back.align(b_back.CENTER)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits, tf_resolution])
        self.title.add([b_1920x1080, b_1000x600, b_800x600, b_back])
