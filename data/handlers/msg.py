""" This module provides message handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

import pygame
import data.eventcodes as ecodes
from data.forms.infobox import InfoBox
from data.interfaces.messagebox import PlainMessageBox, MessageBoxButton


class Message(object):
    def __init__(self, sprite_sheet_handler, sprite_sheet_key) -> None:
        """ Initializes the message handler.

        :param sprite_sheet_handler: sprite sheet handler instance
        :param sprite_sheet_key: sprite sheet key
        """
        self._info_boxes = pygame.sprite.Group()
        self._msgBox = None
        self._msg_cb_event = {}
        self._sprite_sheet_handler = sprite_sheet_handler
        self._sprite_sheet_key = sprite_sheet_key
        # padding top for info boxes
        self.top = 0

    def info(self, text: str) -> None:
        """ Adds an info box to the queue.

        :param text: content that will be shown in the box
        :return: None
        """
        self._info_boxes.add(InfoBox(text, self.top))

    def show(self, caption: str, text: str,
             cb_ok: pygame.event.Event, cb_ok_text: str = 'Ok',
             cb_no: pygame.event.Event = None, cb_no_text: str = 'No') -> None:
        """ Displays a message box.

        :param caption: caption of the message box
        :param text: content of the message box
        :param cb_ok: callback event for Ok/Yes-button
        :param cb_ok_text: text for Ok/Yes-button
        :param cb_no: callback event for No-button
        :param cb_no_text: text for No-button
        :return: None
        """
        self._msg_cb_event['OK'] = cb_ok
        self._msg_cb_event['NO'] = cb_no
        no_btn = None
        ok_btn = MessageBoxButton(cb_ok_text,
                                  pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_MSG_OK),
                                  self._sprite_sheet_handler, self._sprite_sheet_key)
        if cb_no is not None:
            no_btn = MessageBoxButton(cb_no_text,
                                      pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_MSG_NO),
                                      self._sprite_sheet_handler, self._sprite_sheet_key)

        self._msgBox = PlainMessageBox(caption, text, ok_btn, no_btn)

    def is_msg(self) -> bool:
        """ Checks if a message box is active.

        :return: true if a message box is active
        """
        if self._msgBox is not None:
            return True

        return False

    def handle_event(self, event: pygame.event.Event) -> None:
        """ Checks for message box events, raises and handles message box button events.

        :param event: pygame event
        :return: None
        """
        if event.type == ecodes.RESA_TITLE_EVENT:
            if event.code == ecodes.RESA_MSG_OK:
                pygame.event.post(self._msg_cb_event['OK'])
                self._msgBox = None
            elif event.code == ecodes.RESA_MSG_NO:
                pygame.event.post(self._msg_cb_event['NO'])
                self._msgBox = None
            else:
                pass

        if self.is_msg():
            self._msgBox.handle_event(event)

    def run_logic(self) -> None:
        """ Runs logic of info and message boxes.

        :return: None
        """
        self._info_boxes.update()

        if self.is_msg():
            self._msgBox.run_logic()

    def render(self, surface: pygame.Surface) -> None:
        """ Renders all boxes on given surface.

        :param surface: surface to render boxes on
        :return:
        """
        self._info_boxes.draw(surface)

        if self.is_msg():
            self._msgBox.render(surface)
