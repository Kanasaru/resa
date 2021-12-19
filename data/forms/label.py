""" This module provides labels as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.forms.form import Form


class Label(Form):
    def __init__(self, position: tuple[int, int],
                 text: str = "", font_size: int = conf.std_font_size, callback=None) -> None:
        """ Initializes a text box form object

        :param position: position of the textbox on the title
        :param text: displayed text
        :param font_size: font size of displayed text
        :param callback: callback function which is called on update
        """
        Form.__init__(self, (0, 0))

        self.pos_x = position[0]
        self.pos_y = position[1]
        self.text = text
        self.font = None
        self.font_size = font_size
        self.font_colors = {
            "standard": conf.COLOR_BLACK,
        }
        self.callback = callback

        self.set_font(False, self.font_size)
        self.render_text()

    def set_font(self, font: str | bool, size: int = 0) -> None:
        """ Sets the font of the textbox

        :param font: pathname to font that should be used
        :param size: font size of displayed text
        :return: None
        """
        if size != 0:
            self.font_size = size
        if font:
            self.font = pygame.font.Font(font, self.font_size)
        else:
            self.font = pygame.font.SysFont('Arial', self.font_size)

        self.render_text()

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
