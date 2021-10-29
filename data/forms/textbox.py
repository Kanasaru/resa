import pygame
import data.helpers.attr
from data import settings

LEFT = 0
RIGHT = 1
CENTER = 2


class Textbox(pygame.sprite.Sprite):
    def __init__(self, name, attributes=None):
        pygame.sprite.Sprite.__init__(self)

        self.events = []
        self.attr = {
            "name": name,
            "pos_x": 0,
            "pos_y": 0,
            "text": "Textbox",
            "text_font": None,
            "font_size": 20,
            "font_color": settings.COLOR_BLACK,
            "alignment": LEFT,
            "update_text_cb": None,
        }
        if attributes is not None:
            self.set_attr(attributes)

        if self.attr["text_font"] is not None:
            self.font = pygame.font.Font(self.attr["text_font"], self.attr["font_size"])
        else:
            self.font = pygame.font.Font(None, self.attr["font_size"])

        self.update()

    def set_attr(self, attributes):
        return data.helpers.attr.set_attr(self.attr, attributes)

    def get_attr(self, key=None):
        return data.helpers.attr.get_attr(self.attr, key)

    def update(self):
        if self.attr["update_text_cb"] is not None:
            self.attr["text"] = self.attr["update_text_cb"]()

        self.image = self.font.render(self.attr["text"], True, self.attr["font_color"])
        self.rect = self.image.get_rect(topleft=(self.attr["pos_x"], self.attr["pos_y"]))

        if self.attr["alignment"] == RIGHT:
            self.rect.left = self.attr["pos_x"] - self.width()
        elif self.attr["alignment"] == CENTER:
            self.rect.left = self.attr["pos_x"] - self.width() / 2
        else:
            self.rect.top = self.attr["pos_y"]
            self.rect.left = self.attr["pos_x"]

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events.clear()

    def handle_event(self, event):
        return

    def get_dimensions(self):
        return self.image.get_size()

    def width(self):
        return self.image.get_width()

    def height(self):
        return self.image.get_height()
