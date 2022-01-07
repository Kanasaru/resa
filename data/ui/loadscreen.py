""" This module provides the GameLoadScreen class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import data.ui.form as forms
import data.locales as locales


class GameLoadScreen(forms.Interface):
    def __init__(self, cb=None):
        super().__init__()

        self.rect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self._text = f"{locales.get('info_loading_screen')}"

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        tf_load_screen = forms.Label((self.title.width() // 2, self.title.height() // 2), self.text, 20, cb)
        tf_load_screen.font_color(forms.COLOR_WHITE)
        tf_load_screen.align(forms.CENTER)

        self.title.add(tf_load_screen)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value
