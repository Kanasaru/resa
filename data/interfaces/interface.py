""" This module provides the interface base class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

import pygame
from data.forms.title import Title


class Interface(object):
    """Base class for interfaces. Should not be used directly.

    :raises TypeError: if a method is called without assigning a title or assigned title is not <object> Title(Form)
    """
    def __init__(self):
        self._title = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: Title):
        if isinstance(value, Title):
            self._title = value
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def get_events(self):
        if self.__bool__():
            return self.title.get_events()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def handle_event(self, event: pygame.event.Event):
        if self.__bool__():
            self.title.handle_event(event)
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def clear_events(self):
        if self.__bool__():
            self.title.clear_events()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def run_logic(self):
        if self.__bool__():
            self.title.run_logic()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def render(self, surface: pygame.Surface):
        if self.__bool__():
            self.title.render(surface)
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def __bool__(self):
        if isinstance(self.title, Title):
            return True
        return False
