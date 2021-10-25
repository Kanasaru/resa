import pygame
import data.helpers.attr


class Title(object):
    def __init__(self, attributes=None):
        self.attr = {
            "pos_x": 0,
            "pos_y": 0,
            "width": 0,
            "height": 0,
            "bg_color": (255, 255, 255),
            "colorkey": None
        }
        if attributes is not None:
            self.set_attr(attributes)

        self.surface = pygame.Surface((self.attr["width"], self.attr["height"]))
        self.form_objects = pygame.sprite.Group()
        self.events = []

    def set_attr(self, attributes):
        return data.helpers.attr.set_attr(self.attr, attributes)

    def get_attr(self, key=None):
        return data.helpers.attr.get_attr(self.attr, key)

    def add(self, form_object):
        self.form_objects.add(form_object)

    def get_events(self):
        for form_object in self.form_objects:
            self.events.extend(form_object.get_events())
            form_object.clear_events()

        return self.events

    def clear_events(self):
        self.events.clear()

    def handle_event(self, event):
        for form_object in self.form_objects:
            form_object.handle_event(event)

    def run_logic(self):
        self.form_objects.update()

    def render(self, surface):
        self.surface.fill(self.attr["bg_color"])
        if self.attr["colorkey"] is not None:
            self.surface.set_colorkey(self.attr["colorkey"])

        self.form_objects.draw(self.surface)

        pygame.Surface.blit(surface, self.surface, (self.attr["pos_x"], self.attr["pos_y"]))