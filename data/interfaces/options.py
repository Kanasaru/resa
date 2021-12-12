""" This module provides the MainMenu class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button
import data.eventcodes as ecodes


class Options(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.name = 'options'
        self.rect = pygame.Rect((0, 0), conf.resolution)
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = conf.background_image
        self.__credits = f'Created and Designed by {conf.author} | {conf.www}'

        self.build()

    def build(self):
        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)

        # labels
        tf_headline = Label('tf_headline', (int(self.title.width() / 2), 20), conf.title.upper())
        tf_headline.set_font(conf.std_font, 90)
        tf_headline.align(tf_headline.CENTER)
        tf_version = Label('tf_version', (self.title.width() - 5, 5), f'v{conf.version}')
        tf_version.set_font(conf.std_font, 14)
        tf_version.align(tf_version.RIGHT)
        tf_credits = Label('tf_credits', (int(self.title.width() / 2), self.title.height() - 24), self.__credits)
        tf_credits.set_font(conf.std_font, 14)
        tf_credits.align(tf_credits.CENTER)
        width, height = tf_headline.get_dimensions()
        position_y = height + 20
        tf_resolution = Label('tf_resolution', (int(self.title.width() / 2), position_y), 'Resolution')
        tf_resolution.set_font(conf.std_font, 40)
        tf_resolution.align(tf_resolution.CENTER)
        # buttons
        position_y += tf_resolution.height() + 20
        b_1920x1080 = Button(
            'b_1920x1080',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '1920x1080',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_CHG_RESOLUTION, res=(1920, 1080))
        )
        b_1920x1080.set_font(conf.std_font)
        b_1920x1080.align(b_1920x1080.CENTER)
        if conf.resolution == (1920, 1080):
            b_1920x1080.disable()
        position_y += b_1920x1080.height() + 20
        b_1000x600 = Button(
            'b_1000x600',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '1000x600',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_CHG_RESOLUTION, res=(1000, 600))
        )
        b_1000x600.set_font(conf.std_font)
        b_1000x600.align(b_1000x600.CENTER)
        if conf.resolution == (1000, 600):
            b_1000x600.disable()
        position_y += b_1000x600.height() + 20
        b_800x600 = Button(
            'b_800x600',
            pygame.Rect(self.title.width() / 2, position_y, 180, 50),
            self.sheet_handler, self.sheet_key,
            '800x600',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_CHG_RESOLUTION, res=(800, 600))
        )
        b_800x600.set_font(conf.std_font)
        b_800x600.align(b_800x600.CENTER)
        if conf.resolution == (800, 600):
            b_800x600.disable()
        position_y += b_800x600.height() + 20
        b_back = Button(
            'b_back',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Back',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_MAINMENU)
        )
        b_back.set_font(conf.std_font)
        b_back.align(b_back.CENTER)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits, tf_resolution])
        self.title.add([b_1920x1080, b_1000x600, b_800x600, b_back])
