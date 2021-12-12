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


class MainMenu(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.name = 'main'
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
        # buttons
        width, height = tf_headline.get_dimensions()
        position_y = height + 70
        b_newgame = Button(
            'b_newgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'New Game',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_STARTGAME)
        )
        b_newgame.set_font(conf.std_font)
        b_newgame.align(b_newgame.CENTER)
        position_y += b_newgame.height() + 20
        b_loadgame = Button(
            'b_loadgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Load Game',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_LOADGAME)
        )
        b_loadgame.set_font(conf.std_font)
        b_loadgame.align(b_loadgame.CENTER)
        try:
            f = open(conf.save_file)
            f.close()
        except FileNotFoundError:
            b_loadgame.disable()
        position_y += b_loadgame.height() + 20
        b_options = Button(
            'b_option',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Options',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_OPTIONS)
        )
        b_options.set_font(conf.std_font)
        b_options.align(b_options.CENTER)
        position_y += b_options.height() + 20
        b_quitgame = Button(
            'b_quitgame',
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Quit Game',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_QUITGAME)
        )
        b_quitgame.set_font(conf.std_font)
        b_quitgame.align(b_quitgame.CENTER)
        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits])
        self.title.add([b_newgame, b_loadgame, b_options, b_quitgame])
