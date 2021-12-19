""" This module provides buttons as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.forms.form import Form


class Button(Form):
    def __init__(self, rect: pygame.Rect,
                 sprite_sheet_handler: SpriteSheetHandler, sprite_key: str = '',
                 text: str = "", callback_event: pygame.event.Event = None) -> None:
        """ Initializes a button form object

        :param rect: rectangle with dimension and position
        :param sprite_sheet_handler: sprite sheet handler
        :param sprite_key: key of sheet for handler
        :param text: displayed text
        :param callback_event: event which is called if button gets clicked
        """
        Form.__init__(self, rect.size)

        self.COLOR_BUTTON_HOVER = conf.COLOR_BTN_HOVER
        self.COLOR_BUTTON_PRESSED = conf.COLOR_BTN_PRESSED

        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_key

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.text = text
        self.font = None
        self.font_size = conf.std_font_size
        self.font_colors = {
            "standard": conf.COLOR_BLACK,
            "hover": self.COLOR_BUTTON_HOVER,
            "pressed": self.COLOR_BUTTON_PRESSED,
            "disabled": conf.COLOR_BLACK,
        }
        self.surf_images = {}
        self.clickable = True
        self.callback_event = callback_event
        self.button_down = False
        self.colorkey = conf.COLOR_KEY

        self.set_font(False, self.font_size)
        self.load_sprites()
        self.scale()
        self.render_text()
        self.align(self.alignment)
        self.load_start_image()

    def enable(self) -> None:
        """ Enables the button

        :return: None
        """
        self.clickable = True
        self.image = self.surf_images["standard"]

    def disable(self) -> None:
        """ Disables the button

        :return: None
        """
        self.clickable = False
        self.image = self.surf_images["disabled"]

    def toggle(self) -> None:
        """ Toggles the button state for clickable

        :return: None
        """
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

    def set_font(self, font: str | bool, size: int = 0) -> None:
        """ Sets the font of the button

        :param font: pathname to font that should be used
        :param size: font size of displayed text
        :return: None
        """
        if size != 0:
            self.font_size = size
        if font:
            self.font = pygame.font.Font(font, self.font_size)
        else:
            self.font = pygame.font.SysFont('Arial', self.font_size)
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
            "standard": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 0),
            "hover": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 1),
            "pressed": self.sprite_sheet_handler.image_by_index( self.sprite_sheet_key, 2),
            "disabled": self.sprite_sheet_handler.image_by_index( self.sprite_sheet_key, 3)
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
                        pygame.event.post(self.callback_event)
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
