""" This module provides the DebugScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import data.ui.form as forms
import data.locales as locales


class DebugScreen(forms.Interface):
    def __init__(self):
        super().__init__()

        self.clock = pygame.time.Clock()

        self.name = 'debug'
        self.rect = pygame.Rect((0, 0), (pygame.display.get_surface().get_width() // 3,
                                pygame.display.get_surface().get_height()))
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self.alpha = 192

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(self.alpha)

        self._timer = '00:00:00'

        tf_title = forms.Label((15, 40), locales.get('info_debug_title'), 18)
        tf_title.font_color(forms.COLOR_WHITE)
        tf_title.align(forms.LEFT)
        self._y = tf_title.pos_y + tf_title.height() + 10

        tf_playtime = forms.Label((15, self._y), f"{locales.get('info_play_time')}: {self.timer}",
                                  14, self.__update_timer)
        tf_playtime.font_color(forms.COLOR_WHITE)
        tf_playtime.align(forms.LEFT)

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
        new_label = forms.Label((15, self._y), f'{desc}:', 14, lambda: self.__callback(desc, callback))
        new_label.font_color(forms.COLOR_WHITE)
        new_label.align(forms.LEFT)
        self.title.add(new_label)

        self._y = new_label.pos_y + new_label.height() + 10

    def __callback(self, text, func):
        return f'{text}: {func()}'

    def __update_timer(self):
        return f"{locales.get('info_play_time')}: {self.timer}"

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
