""" This module provides the GameLoadScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import data.ui.form as forms
import data.locales as locales


class GamePausedScreen(forms.Interface):
    def __init__(self, rect):
        super().__init__()

        self.rect = rect
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self._text = f"{locales.get('info_game_paused')}"

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(forms.ALPHA)

        l_paused = forms.Label((self.title.width() // 2, self.title.height() // 2), self.text, 20)
        l_paused.font_color(forms.COLOR_WHITE)
        l_paused.align(forms.CENTER)

        self.title.add(l_paused)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value
