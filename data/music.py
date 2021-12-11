from data.settings import conf
import pygame


class Music(object):
    def __init__(self):
        self.pause = False
        self.volume = .2
        self.loop = -1

    def change_volume(self, volume: float) -> None:
        """ Changes the current volume

        :param volume: amount of increase or decrease of current volume
        :return: None
        """
        if 0.0 < volume < 1.0:
            pygame.mixer.music.set_volume(volume)
            self.volume = volume

    def load_music(self) -> None:
        """ Loads the background music into the mixer

        :return: None
        """
        pygame.mixer.music.load(conf.bg_music)

    def start_music(self) -> None:
        """ Starts the background music

        :param volume: volume the music starts at
        :param loop: if true the music plays infinitely
        :return: None
        """
        pygame.mixer.music.play(self.loop)
        pygame.mixer.music.set_volume(self.volume)

    def pause_music(self) -> None:
        """ Toggles background music on and off

        :return: None
        """
        if self.pause:
            pygame.mixer.music.unpause()
            self.pause = False
        else:
            pygame.mixer.music.pause()
            self.pause = True

    def stop_music(self) -> None:
        """ Stops the background music

        :return: None
        """
        pygame.mixer.music.stop()
