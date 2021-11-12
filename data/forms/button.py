import pygame
from data import settings
import data.helpers.attr
import data.helpers.spritesheet
import data.forms.form

LEFT = 0
RIGHT = 1
CENTER = 2


class Button(data.forms.form.Form):
    def __init__(self, name, rect: pygame.Rect, sprite_sheet, sprite_size, attributes=None):
        data.forms.form.Form.__init__(self, rect.size)

        self.set_spritesheet(sprite_sheet, sprite_size)

        # todo: use single methods instead of attr / all attr as param
        self.rect = rect
        self.name = name
        self.attr = {
            "text": "",
            "callback_event": None,
            "clickable": True,
            "text_font": settings.BASIC_FONT,
            "font_size": 20,
            "font_color": settings.COLOR_BLACK,
            "font_color_hover": settings.COLOR_BUTTON_HOVER,
            "font_color_pressed": settings.COLOR_BUTTON_PRESSED,
            "font_color_disabled": settings.COLOR_BLACK,
            "alignment": LEFT,
        }
        if attributes is not None:
            self.set_attr(attributes)

        self.font = pygame.font.Font(self.attr["text_font"], self.attr["font_size"])

        self.surf_images = {
            "image_normal": self.sprite_sheet.image_at(
                (0, 0, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "image_hover": self.sprite_sheet.image_at(
                (0, self.sprite_size[1], self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "image_pressed": self.sprite_sheet.image_at(
                (0, self.sprite_size[1] * 2, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            ),
            "image_disabled": self.sprite_sheet.image_at(
                (0, self.sprite_size[1] * 3, self.sprite_size[0], self.sprite_size[1]),
                self.colorkey
            )
        }

        if self.attr["clickable"]:
            self.image = self.surf_images["image_normal"]
        else:
            self.image = self.surf_images["image_disabled"]

        for key in self.surf_images:
            self.surf_images[key] = pygame.transform.scale(self.surf_images[key], self.rect.size)

        text_surf = self.font.render(self.attr["text"], True, self.attr["font_color"])
        text_surf_hover = self.font.render(self.attr["text"], True, self.attr["font_color_hover"])
        text_surf_pressed = self.font.render(self.attr["text"], True, self.attr["font_color_pressed"])
        text_surf_disabled = self.font.render(self.attr["text"], True, self.attr["font_color_disabled"])

        text_rect = text_surf.get_rect()
        text_pos = self.rect.width / 2 - text_rect.width / 2, self.rect.height / 2 - text_rect.height / 2

        self.surf_images["image_normal"].blit(text_surf, text_pos)
        self.surf_images["image_hover"].blit(text_surf_hover, text_pos)
        self.surf_images["image_pressed"].blit(text_surf_pressed, text_pos)
        self.surf_images["image_disabled"].blit(text_surf_disabled, text_pos)

        if self.attr["alignment"] == RIGHT:
            self.rect.x = self.rect.x - self.rect.width
        elif self.attr["alignment"] == CENTER:
            self.rect.x = self.rect.x - self.rect.width / 2
        else:
            pass

        self.button_down = False

        self.image = self.surf_images["image_normal"]

    def set_attr(self, attributes):
        return data.helpers.attr.set_attr(self.attr, attributes)

    def get_attr(self, key=None):
        return data.helpers.attr.get_attr(self.attr, key)

    def handle_event(self, event):
        if self.attr["clickable"]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.image = self.surf_images["image_pressed"]
                    self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self.button_down:
                    if self.attr["callback_event"] is not None:
                        self.events.append(self.attr["callback_event"])
                    self.image = self.surf_images["image_hover"]
                self.button_down = False
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided and not self.button_down:
                    self.image = self.surf_images["image_hover"]
                elif not collided:
                    self.image = self.surf_images["image_normal"]
        else:
            self.image = self.surf_images["image_disabled"]
