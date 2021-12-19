import pygame
import data.eventcodes as ecodes
from data.forms.infobox import InfoBox
from data.interfaces.messagebox import MessageBox, MessageBoxButton


class Message(object):
    def __init__(self, sprite_sheet_handler, sprite_sheet_key):
        self._info_boxes = pygame.sprite.Group()
        self.top = 0
        self.msg_cb_event = {}
        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_sheet_key
        self.msgBox = None

    def info(self, text: str):
        self._info_boxes.add(InfoBox(text, self.top))

    def show(self, text: str, caption: str,
             cb_ok: pygame.event.Event, cb_ok_text: str = 'Ok',
             cb_no: pygame.event.Event = None, cb_no_text: str = 'No'):
        self.msg_cb_event['OK'] = cb_ok
        self.msg_cb_event['NO'] = cb_no
        ok_button = MessageBoxButton(cb_ok_text,
                                     pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_MSG_OK),
                                     self.sprite_sheet_handler, self.sprite_sheet_key)
        if cb_no is not None:
            no_button = MessageBoxButton(cb_no_text,
                                         pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_MSG_NO),
                                         self.sprite_sheet_handler, self.sprite_sheet_key)
        else:
            no_button = None

        self.msgBox = MessageBox(text, caption, ok_button, no_button)

    def is_msg(self):
        if self.msgBox is not None:
            return True

        return False

    def handle_event(self, event):
        if event.type == ecodes.RESA_TITLE_EVENT:
            if event.code == ecodes.RESA_MSG_OK:
                pygame.event.post(self.msg_cb_event['OK'])
            elif event.code == ecodes.RESA_MSG_NO:
                pygame.event.post(self.msg_cb_event['NO'])
            else:
                pass

        if self.is_msg():
            self.msgBox.handle_event(event)

    def run_logic(self):
        self._info_boxes.update()

        if self.is_msg():
            self.msgBox.run_logic()

    def render(self, surface: pygame.Surface):
        self._info_boxes.draw(surface)

        if self.is_msg():
            self.msgBox.render(surface)
