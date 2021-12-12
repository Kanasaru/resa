""" This module provides debug handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame


class DebugHandler(object):
    def __init__(self, mode: int = 0):
        """ Creates a debug handler.

        :param mode: QUIET | LOUD
        """
        self.QUIET = 0
        self.LOUD = 1
        self._mode = mode
        self._play_time = pygame.time.get_ticks()

    @property
    def mode(self) -> int:
        return self._mode

    @mode.setter
    def mode(self, value) -> None:
        if value == self.QUIET or value == self.LOUD:
            self._mode = value
        else:
            raise ValueError('Given debug mode is not available.')

    @property
    def play_time(self) -> int:
        return self._play_time

    @play_time.setter
    def play_time(self, time: int) -> None:
        self._play_time = time // 1000

    def update(self) -> None:
        """ Updates the handler information.

        :return: None
        """
        self.play_time = pygame.time.get_ticks()

    def toggle(self) -> None:
        """ Toggles between LOUD and QUIET.

        :return: None
        """
        if self.mode == self.QUIET:
            self.mode = self.LOUD
        else:
            self.mode = self.QUIET

    def __bool__(self):
        if self.mode == self.LOUD:
            return True
        return False
