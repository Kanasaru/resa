""" This module provides text boxes as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'

import pygame
from data.forms.form import Form
from data import settings


class Textbox(Form):
    def __init__(self, name: str, position: tuple[int, int],
                 text: str = "", font_size: int = 20, callback=None) -> None:
        """ Initializes a text box from object

        :param name: name of the textbox
        :param position: position of the textbox on the title
        :param text: displayed text
        :param font_size: font size of displayed text
        :param callback: callback function which is called on update
        """
        Form.__init__(self, (0, 0))

        self.name = name
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.text = text
        self.font = None
        self.font_size = font_size
        self.font_colors = {
            "standard": settings.COLOR_BLACK,
        }
        self.callback = callback

        self.set_font(settings.BASIC_FONT, self.font_size)
        self.render_text()

    def set_font(self, font: str, size: int) -> None:
        """ Sets the font of the textbox

        :param font: pathname to font that should be used
        :param size: font size of displayed text
        :return: None
        """
        self.font = pygame.font.Font(font, size)

    def render_text(self) -> None:
        """ Renders text on its own image

        :return: None
        """
        self.image = self.font.render(self.text, True, self.font_colors["standard"])
        self.rect = self.image.get_rect()

        self.align()

    def font_color(self, color: tuple[int, int, int]) -> None:
        """ Sets the font color of the displayed text

        :param color: RGB color
        :return: None
        """
        self.font_colors['standard'] = color
        self.render_text()

    def update(self) -> None:
        """ Updates the textbox by checking the callback function

        :return: None
        """
        if self.callback is not None:
            self.text = self.callback()
            self.render_text()
            self.align()
