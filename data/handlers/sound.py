""" This module provides sound handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
import os


class SoundHandler(object):
    def __init__(self, auto_load: bool = True) -> None:
        """ Creates a sound handler """
        self.sounds = dict()
        self._volume = .6

        if auto_load:
            self.load()

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value) -> None:
        if 0.0 <= value <= 1.0:
            for key, sound in self.sounds.items():
                self.sounds[key].set_volume(value)
            self._volume = value

    def load(self) -> None:
        """ Loads the sounds into the dictionary

        :return: None
        """
        self.sounds.clear()
        for filename in os.listdir(conf.sounds):
            if filename.endswith(".wav") or filename.endswith(".mp3"):
                file = filename
                key = file[:len(file) - 4]
                self.sounds[key] = pygame.mixer.Sound(f'{conf.sounds}/{file}')
                self.sounds[key].set_volume(self.volume)

    def play(self, key: str) -> None:
        """ Plays specific sound

        :param key: key of the sound
        :return: None
        """
        if key in self.sounds:
            self.sounds[key].play()
