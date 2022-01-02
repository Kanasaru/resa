""" This module provides message boxes as interfaces

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
from data.forms.rect import Recty
from data.settings import conf
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button


class MessageBoxButton(object):
    def __init__(self, text: str, cb_event: pygame.event.Event,
                 sprite_sheet_handler: SpriteSheetHandler, sprite_key: str):
        """ Dataclass for message box buttons.

        :param text: text for the button
        :param cb_event: callback event if clicked
        :param sprite_sheet_handler: sprite sheet handler instance
        :param sprite_key: sprite sheet key
        """
        self.text = text
        self.event = cb_event
        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_key


class PlainMessageBox(Interface):
    def __init__(self, caption: str, text: str, btn_yes: MessageBoxButton, btn_no: MessageBoxButton = None):
        """ Creates a message box as an interface.

        :param caption: caption/title of the message box
        :param text: content of the message box
        :param btn_yes: message box button for Ok/Yes-Button
        :param btn_no: optional message box button (No-button)
        """
        super().__init__()

        # set of positioning helpers
        button_width = conf.msg_btn_width
        button_height = conf.msg_btn_height
        button_padding = conf.msg_btn_padding
        border_width = conf.msg_border_width

        # colors
        border_color = conf.COLOR_BLACK
        text_rect_color = conf.COLOR_GRAY
        text_color = conf.COLOR_WHITE
        caption_color = conf.COLOR_WHITE

        # create labels
        self.text = Label((0, 0), text)
        self.text.set_font(conf.std_font, conf.msg_font_size)
        self.text.font_color(caption_color)
        text_width, text_height = self.text.rect.size

        self.caption = Label((0, 0), caption)
        self.caption.set_font(conf.std_font, conf.msg_font_size)
        self.caption.font_color(text_color)
        caption_width, caption_height = self.caption.rect.size

        # calc title size
        title_height = 3 * border_width + caption_height + text_height + 2 * button_padding + button_height
        title_width_1 = 2 * border_width + caption_width
        title_width_2 = 2 * border_width + text_width
        title_width_3 = 2 * border_width + 3 * button_padding + 2 * button_width
        title_width = max([title_width_1, title_width_2, title_width_3])

        self.title_rect = pygame.Rect(((conf.resolution[0] - title_width) // 2,
                                       (conf.resolution[1] - title_height) // 2),
                                      (title_width, title_height))

        # create title
        self.title = Title(self.title_rect, border_color)
        self.title.set_alpha(255)

        # fit labels onto title
        self.caption.pos_x = title_width // 2
        self.caption.pos_y = border_width
        self.text.pos_x = title_width // 2
        self.text.pos_y = 2 * border_width + caption_height
        self.caption.align(self.caption.CENTER)
        self.text.align(self.text.CENTER)

        # create a colored rect as background
        self.text_surface = Recty(pygame.Rect(
            border_width,
            2 * border_width + caption_height,
            title_width - border_width * 2,
            title_height - 3 * border_width - caption_height
        ), text_rect_color)

        # create buttons
        if btn_no is not None:
            b_yes = Button(
                pygame.Rect((border_width + button_padding,
                             title_height - border_width - button_padding - button_height),
                            (button_width, button_height)),
                btn_yes.sprite_sheet_handler,
                btn_yes.sprite_sheet_key,
                btn_yes.text,
                btn_yes.event
            )
            b_yes.set_font(conf.std_font, 13)
            b_yes.align(b_yes.LEFT)

            b_no = Button(
                pygame.Rect((title_width - border_width - button_padding,
                             title_height - border_width - button_padding - button_height),
                            (button_width, button_height)),
                btn_no.sprite_sheet_handler,
                btn_no.sprite_sheet_key,
                btn_no.text,
                btn_no.event
            )
            b_no.set_font(conf.std_font, 13)
            b_no.align(b_no.RIGHT)
        else:
            b_yes = Button(
                pygame.Rect((title_width // 2,
                             title_height - border_width - button_padding - button_height),
                            (button_width, button_height)),
                btn_yes.sprite_sheet_handler,
                btn_yes.sprite_sheet_key,
                btn_yes.text,
                btn_yes.event
            )
            b_yes.set_font(conf.std_font, 13)
            b_yes.align(b_yes.CENTER)

        # add everything to the title
        self.title.add(self.text_surface)
        self.title.add([self.caption, self.text, b_yes])
        if btn_no is not None:
            self.title.add(b_no)
