from data.forms.rect import Recty
from data.settings import conf
import logging
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button


class MessageBoxButton(object):
    def __init__(self, text: str, cb_event: pygame.event.Event,
                 sprite_sheet_handler: SpriteSheetHandler, sprite_key: str):
        self.text = text
        self.event = cb_event
        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_key


class MessageBox(Interface):
    def __init__(self, text: str, caption: str, btn_yes: MessageBoxButton, btn_no: MessageBoxButton = None):
        super().__init__()

        self.caption_padding = 2
        self.text_padding = 5
        self.bg_color = conf.COLOR_BLACK
        self.border_width = 3
        self.button_size = (70, 24)

        # create labels
        self.text = Label((0, 0), text)
        self.text.set_font(conf.std_font, conf.msg_font_size)
        self.text.font_color(conf.COLOR_WHITE)

        self.caption = Label((0, 0), caption)
        self.caption.set_font(conf.std_font, conf.msg_font_size)
        self.caption.font_color(conf.COLOR_WHITE)

        height = self.border_width * 2 + self.caption_padding * 2 + self.caption.rect.height + self.text.rect.height
        height += self.button_size[1] + 10
        if self.caption.rect.width < self.text.rect.width:
            width = self.text.rect.width
        else:
            width = self.caption.rect.width
        width += self.border_width * 2 + self.text_padding * 2

        self.rect = pygame.Rect(((conf.resolution[0] - width) // 2, (conf.resolution[1] - height) // 2), (width, height))
        self.bg_image = None

        self.title = Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        self.caption.pos_x = width // 2
        self.caption.pos_y = self.caption_padding
        self.text.pos_x = width // 2
        self.text.pos_y = self.caption_padding * 2 + self.caption.rect.height
        self.caption.align(self.caption.CENTER)
        self.text.align(self.text.CENTER)

        self.text_surface = Recty(pygame.Rect(
            self.border_width,
            self.caption_padding * 2 + self.caption.rect.height - self.border_width,
            width - self.border_width * 2,
            height - self.caption_padding * 2 - self.caption.rect.height
        ), conf.COLOR_GRAY)

        # buttons
        b_yes = Button(
            pygame.Rect((self.rect.width // 2, self.rect.height - 30), self.button_size),
            btn_yes.sprite_sheet_handler,
            btn_yes.sprite_sheet_key,
            btn_yes.text,
            btn_yes.event
        )
        b_yes.set_font(conf.std_font, 13)
        b_yes.align(b_yes.CENTER)

        self.title.add(self.text_surface)
        self.title.add([self.caption, self.text, b_yes])
