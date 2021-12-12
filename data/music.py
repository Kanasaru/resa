from data.settings import conf
import pygame
import os


class Music(object):
    def __init__(self):
        self.pause = False
        self._volume = .2
        self.loop = 0
        self.playlist = list()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if 0.0 < value < 1.0:
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

        pygame.mixer.music.load(self.playlist.pop())
        pygame.mixer.music.queue(self.playlist.pop())

    def start(self, volume: float) -> None:
        """ Starts the background music

        :param volume: volume the music starts at
        :param loop: if true the music plays infinitely
        :return: None
        """
        pygame.mixer.music.play(self.loop)
        pygame.mixer.music.set_volume(volume)

    def pause(self) -> None:
        """ Toggles background music on and off

        :return: None
        """
        if self.pause:
            pygame.mixer.music.unpause()
            self.pause = False
        else:
            pygame.mixer.music.pause()
            self.pause = True

    def stop(self) -> None:
        """ Stops the background music

        :return: None
        """
        pygame.mixer.music.stop()
