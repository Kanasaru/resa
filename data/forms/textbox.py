"""
This module contains constants, functions and classes for handling textboxes.

:class Textbox: creates a textbox
"""
import pygame
import data.helpers.attr


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
            "font_color": (255, 255, 255),
            "bg_color": (1, 0, 0),
            "colorkey": (1, 0, 0),
            "position": None,
            "update_text_cb": None,
        }
        if attributes is not None:
            self.set_attr(attributes)

        self.update()

    def set_attr(self, attributes):
        return data.helpers.attr.set_attr(self.attr, attributes)

    def get_attr(self, key=None):
        return data.helpers.attr.get_attr(self.attr, key)

    def update(self):
        if self.attr["update_text_cb"] is not None:
            self.attr["text"] = self.attr["update_text_cb"]()

        if self.attr["text_font"] is not None:
            self.font = pygame.font.Font(self.attr["text_font"], self.attr["font_size"])
        else:
            self.font = pygame.font.Font(None, self.attr["font_size"])

        text_width, text_height = self.font.size(self.attr["text"])

        self.image = pygame.Surface((text_width, text_height))
        self.image.fill(self.attr["bg_color"])
        self.image.set_colorkey(self.attr["colorkey"])

        self.rect = self.image.get_rect(topleft=(self.attr["pos_x"], self.attr["pos_y"]))

        text_surf = self.font.render(self.attr["text"], True, self.attr["font_color"])
        text_rect = text_surf.get_rect()

        self.image.blit(text_surf, text_rect)

        if self.attr["position"] == "right":
            self.rect.left = self.attr["pos_x"] - self.width()
        elif self.attr["position"] == "center":
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
