""" This module provides the interface base class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame
from data.forms.title import Title


class Interface(object):
    """Base class for interfaces. Should not used directly.

    :raises TypeError: if a method is called without assigning a title or assigned title is not <object> Title(Form)
    """
    def __init__(self):
        self._name = None
        self._title = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

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

    def handle_event(self, event):
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

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'Interface: {self.name}'

    def __repr__(self):
        return f'Interface: {self.name}'

    def __bool__(self):
        if isinstance(self.title, Title) and self.name is not None:
            return True
        return False
