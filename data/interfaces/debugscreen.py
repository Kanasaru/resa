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


class DebugScreen(Interface):
    def __init__(self):
        super().__init__()

        self.clock = pygame.time.Clock()

        self.name = 'debug'
        self.rect = pygame.Rect((0, 0), (int(conf.resolution[0] / 3), conf.resolution[1]))
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = None
        self.alpha = 192

        self.title = Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(self.alpha)

        self._timer = '00:00:00'

        tf_title = Label((15, 40), f'Debug Screen', 18)
        tf_title.font_color(conf.COLOR_WHITE)
        tf_title.align(tf_title.LEFT)

        self._y = tf_title.pos_y + tf_title.height() + 10

        tf_playtime = Label((15, self._y), f'Current play game: {self.timer}', 14, self.__update_timer)
        tf_playtime.font_color(conf.COLOR_WHITE)
        tf_playtime.align(tf_playtime.LEFT)

        self._y = tf_playtime.pos_y + tf_playtime.height() + 10

        self.title.add(tf_title)
        self.title.add(tf_playtime)

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value: int):
        self._timer = self.seconds_to_clock(value)

    def add(self, desc: str, callback):
        new_label = Label((15, self._y), f'{desc}:', 14, lambda: self.__callback(desc, callback))
        new_label.font_color(conf.COLOR_WHITE)
        new_label.align(new_label.LEFT)
        self.title.add(new_label)

        self._y = new_label.pos_y + new_label.height() + 10

    def __callback(self, text, func):
        return f'{text}: {func()}'

    def __update_timer(self):
        return f'Current play game: {self.timer}'

    @staticmethod
    def seconds_to_clock(seconds: int):
        """ Transforms seconds into time string

        :param seconds: seconds to transform
        :returns: clock format like '00:00:00'
        """
        seconds = abs(seconds)
        hours = seconds // 3600
        minutes = (seconds - (hours * 3600)) // 60
        seconds -= (seconds - (hours * 3600)) - (seconds - (minutes * 60))

        if hours < 10:
            hours = "0" + str(hours)
        else:
            hours = str(hours)
        if minutes < 10:
            minutes = "0" + str(minutes)
        else:
            minutes = str(minutes)
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)

        return f'{hours}:{minutes}:{seconds}'
