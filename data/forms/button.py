import pygame
import data.forms.form
from data import settings

LEFT = 0
RIGHT = 1
CENTER = 2


class Button(data.forms.form.Form):
    def __init__(self, name: str, rect: pygame.Rect,
                 sprite_sheet: str, sprite_size: tuple[int, int],
                 text: str = "", callback: int = None):
        data.forms.form.Form.__init__(self, rect.size)

        self.set_spritesheet(sprite_sheet, sprite_size)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.name = name
        self.text = text
        self.font = settings.BASIC_FONT
        self.font_size = 20
        self.font_color = {
            "standard": settings.COLOR_BLACK,
            "hover": settings.COLOR_BUTTON_HOVER,
            "pressed": settings.COLOR_BUTTON_PRESSED,
            "disabled": settings.COLOR_BLACK,
        }
        self.alignment = LEFT
        self.surf_images = {}
        self.clickable = True
        self.callback_event = callback
        self.button_down = False

        self.set_font(settings.BASIC_FONT, self.font_size)
        self.load_sprites()
        self.scale()
        self.render_text()
        self.align(self.alignment)
        self.load_start_image()

    def enable(self):
        self.clickable = True
        self.image = self.surf_images["standard"]

    def disable(self):
        self.clickable = False
        self.image = self.surf_images["disabled"]

    def toggle(self):
        if self.clickable:
            self.disable()
        else:
            self.enable()

    def load_start_image(self):
        if self.clickable:
            self.image = self.surf_images["standard"]
        else:
            self.image = self.surf_images["disabled"]

    def set_callback_event(self, event: int):
        self.callback_event = event

    def set_font(self, font: str, size: int):
        self.font = pygame.font.Font(font, size)
        self.load_sprites()
        self.scale()
        self.render_text()
        self.load_start_image()

    def scale(self):
        for key in self.surf_images:
            self.surf_images[key] = pygame.transform.scale(self.surf_images[key], self.rect.size)

    def load_sprites(self):
        self.surf_images = {
            "standard": self.sprite_sheet.image_at(
                (0, 0, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "hover": self.sprite_sheet.image_at(
                (0, self.sprite_size[1], self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "pressed": self.sprite_sheet.image_at(
                (0, self.sprite_size[1] * 2, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "disabled": self.sprite_sheet.image_at(
                (0, self.sprite_size[1] * 3, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            )
        }

    def render_text(self):
        text_surf = self.font.render(self.text, True, self.font_color["standard"])
        text_surf_hover = self.font.render(self.text, True, self.font_color["hover"])
        text_surf_pressed = self.font.render(self.text, True, self.font_color["pressed"])
        text_surf_disabled = self.font.render(self.text, True, self.font_color["disabled"])

        text_rect = text_surf.get_rect()
        text_pos = self.rect.width / 2 - text_rect.width / 2, self.rect.height / 2 - text_rect.height / 2

        self.surf_images["standard"].blit(text_surf, text_pos)
        self.surf_images["hover"].blit(text_surf_hover, text_pos)
        self.surf_images["pressed"].blit(text_surf_pressed, text_pos)
        self.surf_images["disabled"].blit(text_surf_disabled, text_pos)

    def align(self, alignment: int):
        if alignment == self.alignment:
            pass
        elif alignment == RIGHT:
            self.rect.x = self.pos_x - self.rect.width
        elif alignment == CENTER:
            self.rect.x = self.pos_x - self.rect.width / 2
        elif alignment == LEFT:
            self.rect.x = self.pos_x

    def handle_event(self, event):
        if self.clickable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.image = self.surf_images["pressed"]
                    self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self.button_down:
                    if self.callback_event is not None:
                        self.events.append(self.callback_event)
                    self.image = self.surf_images["hover"]
                self.button_down = False
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided and not self.button_down:
                    self.image = self.surf_images["hover"]
                elif not collided:
                    self.image = self.surf_images["standard"]
        else:
            self.image = self.surf_images["disabled"]
