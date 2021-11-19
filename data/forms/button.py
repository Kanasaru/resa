""" This module provides buttons as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'

import pygame
from data.forms.form import Form
from data import settings


class Button(Form):
    def __init__(self, name: str, rect: pygame.Rect,
                 sprite_sheet: str, sprite_size: tuple[int, int],
                 text: str = "", callback_event: object = None) -> None:
        Form.__init__(self, rect.size)

        self.set_spritesheet(sprite_sheet, sprite_size)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.name = name
        self.text = text
        self.font = None
        self.font_size = 20
        self.font_colors = {
            "standard": settings.COLOR_BLACK,
            "hover": settings.COLOR_BUTTON_HOVER,
            "pressed": settings.COLOR_BUTTON_PRESSED,
            "disabled": settings.COLOR_BLACK,
        }
        self.surf_images = {}
        self.clickable = True
        self.callback_event = callback_event
        self.button_down = False

        self.set_font(settings.BASIC_FONT, self.font_size)
        self.load_sprites()
        self.scale()
        self.render_text()
        self.align(self.alignment)
        self.load_start_image()

    def enable(self) -> None:
        self.clickable = True
        self.image = self.surf_images["standard"]

    def disable(self) -> None:
        self.clickable = False
        self.image = self.surf_images["disabled"]

    def toggle(self) -> None:
        if self.clickable:
            self.disable()
        else:
            self.enable()

    def load_start_image(self) -> None:
        """ Sets the starting image of the button

        :return: None
        """
        if self.clickable:
            self.image = self.surf_images["standard"]
        else:
            self.image = self.surf_images["disabled"]

    def set_callback_event(self, event) -> None:
        """ Sets the callback event which is return to the title if button was clicked

        :param event: resa event
        :return: None
        """
        self.callback_event = event

    def set_font(self, font: str, size: int) -> None:
        """ Sets the font of the button

        :param font: pathname to font that should be used
        :param size: font size of displayed text
        :return: None
        """
        self.font = pygame.font.Font(font, size)
        self.load_sprites()
        self.scale()
        self.render_text()
        self.load_start_image()

    def scale(self) -> None:
        """ Scales individual sprites from sprite sheet for each button state to button size

        :return: None
        """
        for key in self.surf_images:
            self.surf_images[key] = pygame.transform.scale(self.surf_images[key], self.rect.size)

    def load_sprites(self) -> None:
        """ Loads individual sprites from sprite sheet for each button state

        :return: None
        """
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

    def render_text(self) -> None:
        """ Renders text for all button states on their images

        :return: None
        """
        text_surf = self.font.render(self.text, True, self.font_colors["standard"])
        text_surf_hover = self.font.render(self.text, True, self.font_colors["hover"])
        text_surf_pressed = self.font.render(self.text, True, self.font_colors["pressed"])
        text_surf_disabled = self.font.render(self.text, True, self.font_colors["disabled"])

        text_rect = text_surf.get_rect()
        text_pos = self.rect.width / 2 - text_rect.width / 2, self.rect.height / 2 - text_rect.height / 2

        self.surf_images["standard"].blit(text_surf, text_pos)
        self.surf_images["hover"].blit(text_surf_hover, text_pos)
        self.surf_images["pressed"].blit(text_surf_pressed, text_pos)
        self.surf_images["disabled"].blit(text_surf_disabled, text_pos)

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event
        :return: None
        """
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
