""" This module provides music handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import random
from data.settings import conf
import data.eventcodes as ecodes
import pygame
import os


class Music(object):
    def __init__(self) -> None:
        """ Creates a music handler """
        self.paused = False
        self._volume = .2
        self.loop = 0
        self.playlist = list()
        self.shuffle = True

        # set event for music ending
        pygame.mixer.music.set_endevent(ecodes.RESA_MUSIC_ENDED_EVENT)

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value) -> None:
        if 0.0 <= value <= 1.0:
            pygame.mixer.music.set_volume(value)
            self._volume = value

    def load(self) -> None:
        """ Loads the background music into the mixer

        :return: None
        """
        for filename in os.listdir(conf.bg_music):
            if filename.endswith(".mp3"):
                file = filename
                self.playlist.append(f'{conf.bg_music}/{file}')

        if self.shuffle:
            random.shuffle(self.playlist)

        pygame.mixer.music.load(self.playlist.pop())
        pygame.mixer.music.queue(self.playlist.pop())

    def load_next(self) -> None:
        """ Loads the next piece into the queue.

        :return: None
        """
        pygame.mixer.music.queue(self.playlist.pop())

    def refill(self) -> None:
        """ Refills the playlist and fills the queue with the first piece.

        :return: None
        """
        for filename in os.listdir(conf.bg_music):
            if filename.endswith(".mp3"):
                file = filename
                self.playlist.append(f'{conf.bg_music}/{file}')

        if self.shuffle:
            random.shuffle(self.playlist)

        pygame.mixer.music.queue(self.playlist.pop())

    def start(self, volume: float) -> None:
        """ Starts the background music

        :param volume: volume the music starts with
        :return: None
        """
        pygame.mixer.music.play(self.loop)
        pygame.mixer.music.set_volume(volume)

    def pause(self) -> None:
        """ Toggles background music on and off

        :return: None
        """
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    @staticmethod
    def stop() -> None:
        """ Stops the background music

        :return: None
        """
        pygame.mixer.music.stop()
