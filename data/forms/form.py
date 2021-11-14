import pygame
import data.helpers.spritesheet
from data import settings


class Form(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        self.LEFT = 0
        self.RIGHT = 1
        self.CENTER = 2

        self.image = pygame.Surface(size)
        self.image.fill(settings.COLOR_WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0
        self.pos_x = 0
        self.pos_y = 0
        self.alignment = self.LEFT

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

    def align(self, alignment: int = None):
        if alignment is None:
            alignment = self.alignment

        if alignment == self.RIGHT:
            self.rect.x = self.pos_x - self.rect.width
            self.rect.y = self.pos_y
        elif alignment == self.CENTER:
            self.rect.x = self.pos_x - self.rect.width / 2
            self.rect.y = self.pos_y
        elif alignment == self.LEFT:
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y

        self.alignment = alignment
