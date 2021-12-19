import pygame
from data.forms.infobox import InfoBox


class Message(object):
    def __init__(self):
        self._boxes = pygame.sprite.Group()
        self.top = 0

    def info(self, text: str):
        self._boxes.add(InfoBox(text, self.top))

    def run_logic(self):
        self._boxes.update()

    def render(self, surface: pygame.Surface):
        self._boxes.draw(surface)
