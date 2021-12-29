""" This module provides switches as form objects that can be used in titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

from data.settings import conf
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.forms.form import Form


class Switch(Form):
    def __init__(self, rect: pygame.Rect,
                 sprite_sheet_handler: SpriteSheetHandler, sprite_key: str,
                 callback_event_active: pygame.event.Event,
                 callback_event_inactive: pygame.event.Event,
                 active: bool = True) -> None:
        """ Initializes a switch form object

        :param rect: rectangle with dimension and position
        :param sprite_sheet_handler: sprite sheet handler
        :param sprite_key: key of sheet for handler
        :param callback_event_active: event which is called if switch gets activated
        :param callback_event_inactive: event which is called if switch gets inactivated
        :param active: default state of the switch
        """
        Form.__init__(self, rect.size)

        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_key

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.surf_images = {}
        self.clickable = True
        self.cb_event_active = callback_event_active
        self.cb_event_inactive = callback_event_inactive
        self.active = active
        self.colorkey = conf.COLOR_KEY

        self.load_sprites()
        self.scale()
        self.align(self.alignment)
        self.load_start_image()

    def enable(self) -> None:
        """ Enables the switch

        :return: None
        """
        self.clickable = True
        self.image = self.surf_images["active"]

    def disable(self) -> None:
        """ Disables the switch

        :return: None
        """
        self.clickable = False
        self.image = self.surf_images["inactive"]

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
            if self.active:
                self.image = self.surf_images["active"]
            else:
                self.image = self.surf_images["inactive"]
        else:
            self.image = self.surf_images["disabled"]

    def scale(self) -> None:
        """ Scales individual sprites from sprite sheet for each switch state to switch size

        :return: None
        """
        for key in self.surf_images:
            self.surf_images[key] = pygame.transform.scale(self.surf_images[key], self.rect.size)

    def load_sprites(self) -> None:
        """ Loads individual sprites from sprite sheet for each switch state

        :return: None
        """
        self.surf_images = {
            "active": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 1),
            "hover_active": pygame.transform.rotate(self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 0),
                                                    180),
            "hover_inactive": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 2),
            "inactive": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 0),
            "disabled": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 3)
        }

    def clicked(self) -> None:
        """ Toggles image of the switch and post its state event.

        :return: None
        """
        if self.active:
            self.active = False
            self.image = self.surf_images["inactive"]
            pygame.event.post(self.cb_event_inactive)
        else:
            self.active = True
            self.image = self.surf_images["active"]
            pygame.event.post(self.cb_event_active)

    def handle_event(self, event: pygame.event.Event) -> None:
        """ Handles given event

        :param event: resa event
        :return: None
        """
        if self.clickable:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.clicked()
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided:
                    if self.active:
                        self.image = self.surf_images["hover_active"]
                    else:
                        self.image = self.surf_images["hover_inactive"]
                elif not collided:
                    if self.active:
                        self.image = self.surf_images["active"]
                    else:
                        self.image = self.surf_images["inactive"]
        else:
            self.image = self.surf_images["disabled"]
