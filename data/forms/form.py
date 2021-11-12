import pygame
import data.helpers.spritesheet
from data import settings


class Form(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(settings.COLOR_WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.events = []
        self.sprite_size = (0, 0)
        self.sprite_sheet = None
        self.colorkey = settings.COLOR_KEY

    def set_spritesheet(self, sprite_sheet: str, sprite_size: tuple[int, int]):
        self.sprite_sheet = data.helpers.spritesheet.SpriteSheet(sprite_sheet)
        self.sprite_size = sprite_size

    def set_colorkey(self, key: tuple[int, int, int]):
        self.image.set_colorkey(key)

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events.clear()

    def handle_event(self, event):
        pass

    def get_dimensions(self):
        return self.image.get_size()

    def width(self):
        return self.image.get_width()

    def height(self):
        return self.image.get_height()
