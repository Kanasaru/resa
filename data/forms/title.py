import pygame
import data.forms.form
from data import settings


class Title(data.forms.form.Form):
    def __init__(self, name: str, rect: pygame.Rect,
                 bg_color: tuple[int, int, int], bg_image=None,
                 colorkey: tuple[int, int, int] = settings.COLOR_KEY):
        data.forms.form.Form.__init__(self, rect.size)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.name = name
        self.bg_color = bg_color
        self.bg_image = bg_image
        self.colorkey = colorkey

        self.form_objects = pygame.sprite.Group()

        self.bg_img = None
        self.set_bg_image()

    def set_bg_image(self):
        if self.bg_image is not None:
            pic = pygame.image.load(self.bg_image).convert()
            self.bg_img = pygame.transform.scale(pic, pic.get_rect().size)

    def add(self, form_object):
        self.form_objects.add(form_object)

    def get_events(self):
        for form_object in self.form_objects:
            self.events.extend(form_object.get_events())
            form_object.clear_events()

        return self.events

    def handle_event(self, event):
        for form_object in self.form_objects:
            form_object.handle_event(event)

    def run_logic(self):
        self.form_objects.update()

    def render(self, surface):
        self.image.fill(self.bg_color)
        if self.bg_img is not None:
            self.image.blit(self.bg_img, (self.pos_x, self.pos_y))
        if self.colorkey is not None:
            self.image.set_colorkey(self.colorkey)

        self.form_objects.draw(self.image)

        pygame.Surface.blit(surface, self.image, (self.pos_x, self.pos_y))
