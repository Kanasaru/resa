""" This module provides labels as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

from data.settings import conf
import pygame
from data.forms.form import Form


class Recty(Form):
    def __init__(self, rect: pygame.Rect, color) -> None:
        Form.__init__(self, rect.size)

        self.pos_x = rect.x
        self.pos_y = rect.y
        self.rect = rect
        self.image.fill(color)

    def update(self) -> None:
        pass
