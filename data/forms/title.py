import pygame
import data.helpers.attr
from data import settings


class Title(object):
    def __init__(self, name, attributes=None):
        self.attr = {
            "name": name,
            "pos_x": 0,
            "pos_y": 0,
            "width": 0,
            "height": 0,
            "bg_color": settings.COLOR_BLACK,
            "colorkey": None,
            "bg_image": None,
        }
        if attributes is not None:
            self.set_attr(attributes)

        self.surface = pygame.Surface((self.attr["width"], self.attr["height"]))
        self.form_objects = pygame.sprite.Group()
        self.events = []

        self.bg_img = None
        self.set_bg_image()

    def set_attr(self, attributes):
        return data.helpers.attr.set_attr(self.attr, attributes)

    def get_attr(self, key=None):
        return data.helpers.attr.get_attr(self.attr, key)

    def set_bg_image(self):
        if self.get_attr("bg_image") is not None:
            pic = pygame.image.load(self.get_attr("bg_image")).convert()
            self.bg_img = pygame.transform.scale(pic, pic.get_rect().size)

    def set_forms_attr(self, name, attr):
        for form_object in self.form_objects:
            if form_object.get_attr("name") == name:
                form_object.set_attr(attr)
                return True
        return False

    def get_forms_attr(self, name, attr_key):
        for form_object in self.form_objects:
            if form_object.get_attr("name") == name:
                return form_object.get_attr(attr_key)
        return False

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
        if self.bg_img is not None:
            self.surface.blit(self.bg_img, (self.attr["pos_x"], self.attr["pos_y"]))
        if self.attr["colorkey"] is not None:
            self.surface.set_colorkey(self.attr["colorkey"])

        self.form_objects.draw(self.surface)

        pygame.Surface.blit(surface, self.surface, (self.attr["pos_x"], self.attr["pos_y"]))

    def width(self):
        return self.get_attr("width")

    def height(self):
        return self.get_attr("height")
