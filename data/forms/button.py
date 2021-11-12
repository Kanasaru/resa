import pygame
from data import settings
import data.helpers.attr
import data.helpers.spritesheet

LEFT = 0
RIGHT = 1
CENTER = 2


class Button(pygame.sprite.Sprite):
    def __init__(self, name, rect: pygame.Rect, attributes=None):
        pygame.sprite.Sprite.__init__(self)

        # todo: use single methods instead of attr / all attr as param
        self.events = []
        self.rect = rect
        self.attr = {
            "name": name,
            "sprite_size": (220, 60),
            "text": "",
            "callback_event": None,
            "clickable": True,
            "spritesheet": None,
            "text_font": settings.BASIC_FONT,
            "font_size": 20,
            "font_color": settings.COLOR_BLACK,
            "font_color_hover": settings.COLOR_BUTTON_HOVER,
            "font_color_pressed": settings.COLOR_BUTTON_PRESSED,
            "font_color_disabled": settings.COLOR_BLACK,
            "bg_color": settings.COLOR_WHITE,
            "colorkey": settings.COLOR_KEY,
            "alignment": LEFT,
        }
        if attributes is not None:
            self.set_attr(attributes)

        self.font = pygame.font.Font(self.attr["text_font"], self.attr["font_size"])

        self.surf_images = {
            "image_normal": None,
            "image_hover": None,
            "image_pressed": None,
            "image_disabled": None
        }

        if self.attr["spritesheet"] is not None:
            self.spritesheet = data.helpers.spritesheet.SpriteSheet(self.attr["spritesheet"])

            self.surf_images["image_normal"] = self.spritesheet.image_at(
                (0, 0, self.attr["sprite_size"][0], self.attr["sprite_size"][1]), self.attr["colorkey"])
            self.surf_images["image_hover"] = self.spritesheet.image_at(
                (0, self.attr["sprite_size"][1], self.attr["sprite_size"][0], self.attr["sprite_size"][1]), self.attr["colorkey"])
            self.surf_images["image_pressed"] = self.spritesheet.image_at(
                (0, self.attr["sprite_size"][1] * 2, self.attr["sprite_size"][0], self.attr["sprite_size"][1]), self.attr["colorkey"])
            self.surf_images["image_disabled"] = self.spritesheet.image_at(
                (0, self.attr["sprite_size"][1] * 3, self.attr["sprite_size"][0], self.attr["sprite_size"][1]), self.attr["colorkey"])

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

    def update(self):
        pass

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events.clear()

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

    def get_dimensions(self):
        return self.image.get_size()

    def width(self):
        return self.image.get_width()

    def height(self):
        return self.image.get_height()
