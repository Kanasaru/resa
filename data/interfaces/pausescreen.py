""" This module provides the GameLoadScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title


class GamePausedScreen(Interface):
    def __init__(self, rect):
        super().__init__()

        self.name = 'pause_screen'
        self.rect = rect
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = None
        self._text = f'Game paused!'

        self.title = Title(self.name, self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(192)

        l_paused = Label('l_paused', (self.title.width() // 2, self.title.height() // 2), self.text, 20)
        l_paused.set_font(conf.std_font, 20)
        l_paused.font_color(conf.COLOR_WHITE)
        l_paused.align(l_paused.CENTER)

        self.title.add(l_paused)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value
