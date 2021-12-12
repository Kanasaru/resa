""" This module provides a title class which helps to structure and control form objects

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.1'

from data.settings import conf
import pygame
from data.forms.form import Form


class Title(Form):
    def __init__(self, name: str, rect: pygame.Rect,
                 bg_color: tuple[int, int, int], bg_image=None,
                 colorkey: tuple[int, int, int] = conf.COLOR_KEY) -> None:
        """ Initializes a title that handles and arrange other form objects

        :param name: name of the title
        :param rect: position and dimension of the title
        :param bg_color: color to fill the background with
        :param bg_image: pathname to background image
        :param colorkey: colorkey which is used on the title surface
        """
        Form.__init__(self, rect.size)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.name = name
        self.bg_color = bg_color
        self.bg_image = bg_image
        self.colorkey = colorkey
        self.form_objects = pygame.sprite.Group()

        self.set_bg_image(self.bg_image)

    def set_bg_image(self, bg_image: str = None) -> None:
        """ Sets and scales a background image for the title

        :param bg_image: pathname of background image
        :return: None
        """
        self.bg_image = bg_image

        if self.bg_image is not None:
            pic = pygame.image.load(self.bg_image).convert()
            self.bg_image = pygame.transform.scale(pic, self.rect.size)

    def add(self, form_object: Form | list[Form]) -> None:
        """ Adds a form object to the title

        :param form_object: form object that has to be added to the title
        :return: None
        """
        if isinstance(form_object, list):
            for obj in form_object:
                self.form_objects.add(obj)
        else:
            self.form_objects.add(form_object)

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event object
        :return: None
        """
        for form_object in self.form_objects:
            form_object.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the logic methods of all form objects of the title

        :return: None
        """
        self.form_objects.update()

    def render(self, surface: pygame.Surface) -> None:
        """ Renders the title and its form objects to given surface

        :param surface: pygame surface the title will be drawn to
        :return: None
        """
        self.image.fill(self.bg_color)
        if self.bg_image is not None:
            self.image.blit(self.bg_image, (self.pos_x, self.pos_y))
        if self.colorkey is not None:
            self.image.set_colorkey(self.colorkey)

        self.form_objects.draw(self.image)

        pygame.Surface.blit(surface, self.image, (self.pos_x, self.pos_y))
