""" This module provides the DebugScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.helpers.time import seconds_to_clock
import data.helpers.color as colors


class DebugScreen(Interface):
    def __init__(self):
        super().__init__()

        self.clock = pygame.time.Clock()

        self.name = 'debug'
        self.rect = pygame.Rect((0, 0), (int(conf.resolution[0] / 3), conf.resolution[1]))
        self.bg_color = colors.COLOR_BLACK
        self.bg_image = None
        self.alpha = 192

        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(self.alpha)

        self._timer = '00:00:00'

        tf_title = Label('tf_title', (15, 40), f'Debug Screen', 18)
        tf_title.font_color(colors.COLOR_WHITE)
        tf_title.align(tf_title.LEFT)

        self._y = tf_title.pos_y + tf_title.height() + 10

        tf_playtime = Label('tf_playtime', (15, self._y), f'Current play game: {self.timer}', 14, self.__update_timer)
        tf_playtime.font_color(colors.COLOR_WHITE)
        tf_playtime.align(tf_playtime.LEFT)

        self._y = tf_playtime.pos_y + tf_playtime.height() + 10

        self.title.add(tf_title)
        self.title.add(tf_playtime)

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value: int):
        self._timer = seconds_to_clock(value)

    def add(self, desc: str, callback):
        new_label = Label(desc, (15, self._y), f'{desc}:', 14, lambda: self.__callback(desc, callback))
        new_label.font_color(colors.COLOR_WHITE)
        new_label.align(new_label.LEFT)
        self.title.add(new_label)

        self._y = new_label.pos_y + new_label.height() + 10

    def __callback(self, text, func):
        return f'{text}: {func()}'

    def __update_timer(self):
        return f'Current play game: {self.timer}'
