""" This module provides the GameLoadScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title


class GameLoadScreen(Interface):
    def __init__(self, cb=None):
        super().__init__()

        self.name = 'load_screen'
        self.rect = pygame.Rect((0, 0), conf.resolution)
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = None
        self._text = f'Loading world...'

        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        tf_load_screen = Label('tf_load_screen', (self.title.width() // 2, self.title.height() // 2), self.text, 20, cb)
        tf_load_screen.set_font(conf.std_font, 20)
        tf_load_screen.font_color(conf.COLOR_WHITE)
        tf_load_screen.align(tf_load_screen.CENTER)

        self.title.add(tf_load_screen)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value
