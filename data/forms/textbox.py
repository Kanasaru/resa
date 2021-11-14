import pygame
import data.forms.form
from data import settings


class Textbox(data.forms.form.Form):
    def __init__(self, name: str, position: tuple[int, int],
                 text: str = "", font_size: int = 20, callback=None):
        pygame.sprite.Sprite.__init__(self)
        data.forms.form.Form.__init__(self, (0, 0))

        self.name = name
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.text = text
        self.font = None
        self.font_size = font_size
        self.font_colors = {
            "standard": settings.COLOR_BLACK,
        }
        self.callback = callback

        self.set_font(settings.BASIC_FONT, self.font_size)

        self.render_text()

    def set_font(self, font: str, size: int):
        self.font = pygame.font.Font(font, size)

    def render_text(self):
        self.image = self.font.render(self.text, True, self.font_colors["standard"])
        self.rect = self.image.get_rect()

        self.align()

    def font_color(self, color: tuple[int, int, int]):
        self.font_colors['standard'] = color
        self.render_text()

    def update(self):
        if self.callback is not None:
            self.text = self.callback()
            self.render_text()
            self.align()
