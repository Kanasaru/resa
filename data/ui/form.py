""" This module provides form objects

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import data.eventcodes as ecodes
from data.handlers.spritesheet import SpriteSheetHandler
from data.handlers.sound import SoundHandler

LEFT = 0
RIGHT = 1
CENTER = 2

COLOR_KEY = (1, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_GREEN = (0, 128, 0)
COLOR_BTN_HOVER = (120, 117, 98)
COLOR_BTN_PRESSED = (120, 117, 98)
ALPHA = 192

STD_SYSFONT = 'Arial'
STD_FONT_SIZE = 20
MSG_FONT_SIZE = 16

INFOBOX_TIMEOUT = 3000

PATH_SOUNDS = 'resources/sounds'
SOUND_BTN_CLICK = 'btn-click'


class Form(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int]) -> None:
        """ Initializes an 'abstract' class for form objects. Should not be used directly.

        :param size: size of the form object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.pos_x = 0
        self.pos_y = 0
        self.alignment = LEFT
        self.sprite_sheet_handler = None

    def set_alpha(self, value):
        self.image.set_alpha(value)

    def set_colorkey(self, key: tuple[int, int, int]) -> None:
        """ Sets the colorkey of the image

        :param key: color to be set as the colorkey
        :return: None
        """
        self.image.set_colorkey(key)

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event
        :return: None
        """
        pass

    def get_dimensions(self) -> tuple[int, int]:
        """ Returns form dimensions

        :return: size of the form image
        """
        return self.image.get_size()

    def width(self) -> int:
        """ Returns form width

        :return: width of the form image
        """
        return self.image.get_width()

    def height(self) -> int:
        """ Returns form height

        :return: height of the form image
        """
        return self.image.get_height()

    def align(self, alignment: int = None) -> None:
        """ Aligns the form horizontally in relation to its own position

        :param alignment: integer to set right, left or center
        :return: None
        """
        if alignment is None:
            alignment = self.alignment

        if alignment == RIGHT:
            self.rect.x = self.pos_x - self.rect.width
            self.rect.y = self.pos_y
        elif alignment == CENTER:
            self.rect.x = self.pos_x - self.rect.width / 2
            self.rect.y = self.pos_y
        elif alignment == LEFT:
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y

        self.alignment = alignment


class Title(Form):
    def __init__(self, rect: pygame.Rect,
                 bg_color: tuple[int, int, int], bg_image=None,
                 colorkey: tuple[int, int, int] = COLOR_KEY) -> None:
        """ Initializes a title that handles and arrange other form objects

        :param rect: position and dimension of the title
        :param bg_color: color to fill the background with
        :param bg_image: pathname to background image
        :param colorkey: colorkey which is used on the title surface
        """
        Form.__init__(self, rect.size)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.bg_color = bg_color
        self.bg_image = bg_image
        self.colorkey = colorkey
        self.form_objects = pygame.sprite.Group()

        self.set_bg_image(self.bg_image)

    def set_bg_image(self, bg_image: str = None) -> None:
        """ Sets and scales a background image for the title

        :param bg_image: pathname of background image
        :return: None
        """
        self.bg_image = bg_image

        if self.bg_image is not None:
            pic = pygame.image.load(self.bg_image).convert()
            self.bg_image = pygame.transform.scale(pic, self.rect.size)

    def add(self, form_object: Form | list[Form]) -> None:
        """ Adds a form object to the title

        :param form_object: form object that has to be added to the title
        :return: None
        """
        if isinstance(form_object, list):
            for obj in form_object:
                self.form_objects.add(obj)
        else:
            self.form_objects.add(form_object)

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event object
        :return: None
        """
        # relativize mouse position (necessary if title has not full display size)
        if event.type == pygame.MOUSEBUTTONDOWN or \
                event.type == pygame.MOUSEBUTTONUP or \
                event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            x -= self.rect.x
            y -= self.rect.y
            event.pos = x, y

        for form_object in self.form_objects:
            form_object.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the logic methods of all form objects of the title

        :return: None
        """
        self.form_objects.update()

    def render(self, surface: pygame.Surface) -> None:
        """ Renders the title and its form objects to given surface

        :param surface: pygame surface the title will be drawn to
        :return: None
        """
        self.image.fill(self.bg_color)
        if self.bg_image is not None:
            self.image.blit(self.bg_image, (self.pos_x, self.pos_y))
        if self.colorkey is not None:
            self.image.set_colorkey(self.colorkey)

        self.form_objects.draw(self.image)

        pygame.Surface.blit(surface, self.image, (self.pos_x, self.pos_y))


class Interface(object):
    """Base class for interfaces. Should not be used directly.

    :raises TypeError: if a method is called without assigning a title or assigned title is not <object> Title(Form)
    """
    def __init__(self):
        self._title = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: Title):
        if isinstance(value, Title):
            self._title = value
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def get_events(self):
        if self.__bool__():
            return self.title.get_events()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def handle_event(self, event: pygame.event.Event):
        if self.__bool__():
            self.title.handle_event(event)
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def clear_events(self):
        if self.__bool__():
            self.title.clear_events()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def run_logic(self):
        if self.__bool__():
            self.title.run_logic()
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def render(self, surface: pygame.Surface):
        if self.__bool__():
            self.title.render(surface)
        else:
            raise TypeError('title has to be <object> Title(Form)')

    def __bool__(self):
        if isinstance(self.title, Title):
            return True
        return False


class Label(Form):
    def __init__(self, position: tuple[int, int],
                 text: str = "", font_size: int = STD_FONT_SIZE, callback=None) -> None:
        """ Initializes a text box form object

        :param position: position of the textbox on the title
        :param text: displayed text
        :param font_size: font size of displayed text
        :param callback: callback function which is called on update
        """
        Form.__init__(self, (0, 0))

        self.pos_x = position[0]
        self.pos_y = position[1]
        self.text = text
        self.font = None
        self.font_size = font_size
        self.font_colors = {
            "standard": COLOR_BLACK,
        }
        self.callback = callback

        self.set_font(False, self.font_size)
        self.render_text()

    def set_font(self, font: str | bool, size: int = 0) -> None:
        """ Sets the font of the textbox

        :param font: pathname to font that should be used
        :param size: font size of displayed text
        :return: None
        """
        if size != 0:
            self.font_size = size
        if font:
            self.font = pygame.font.Font(font, self.font_size)
        else:
            self.font = pygame.font.SysFont(STD_SYSFONT, self.font_size)

        self.render_text()

    def render_text(self) -> None:
        """ Renders text on its own image

        :return: None
        """
        self.image = self.font.render(self.text, True, self.font_colors["standard"])
        self.rect = self.image.get_rect()

        self.align()

    def font_color(self, color: tuple[int, int, int]) -> None:
        """ Sets the font color of the displayed text

        :param color: RGB color
        :return: None
        """
        self.font_colors['standard'] = color
        self.render_text()

    def update(self) -> None:
        """ Updates the textbox by checking the callback function

        :return: None
        """
        if self.callback is not None:
            self.text = self.callback()
            self.render_text()
            self.align()


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

        self.COLOR_BUTTON_HOVER = COLOR_BTN_HOVER
        self.COLOR_BUTTON_PRESSED = COLOR_BTN_PRESSED

        self.sprite_sheet_handler = sprite_sheet_handler
        self.sprite_sheet_key = sprite_key

        self.sounds = SoundHandler(PATH_SOUNDS)

        self.rect = rect
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.text = text
        self.font = None
        self.font_size = STD_FONT_SIZE
        self.font_colors = {
            "standard": COLOR_BLACK,
            "hover": self.COLOR_BUTTON_HOVER,
            "pressed": self.COLOR_BUTTON_PRESSED,
            "disabled": COLOR_BLACK,
        }
        self.surf_images = {}
        self.clickable = True
        self.callback_event = callback_event
        self.button_down = False
        self.colorkey = COLOR_KEY

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
            self.font = pygame.font.SysFont(STD_SYSFONT, self.font_size)
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
            "pressed": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 2),
            "disabled": self.sprite_sheet_handler.image_by_index(self.sprite_sheet_key, 3)
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
                    self.sounds.play(SOUND_BTN_CLICK)
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
        self.colorkey = COLOR_KEY

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


class InfoBox(Form):
    def __init__(self, text: str, pos_y, display_time: int = INFOBOX_TIMEOUT) -> None:
        Form.__init__(self, (0, 0))

        # render font image
        self.font = pygame.font.Font(None, MSG_FONT_SIZE)
        self.font_image = self.font.render(text, True, COLOR_WHITE)
        self.font_rect = self.font_image.get_rect()

        # create surface and blit message
        self.image = pygame.Surface((self.font_rect.width + 20, self.font_rect.height + 20))
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_BLACK)
        self.image.set_alpha(ALPHA)
        self.image.blit(self.font_image, ((self.rect.width - self.font_rect.width) / 2, 10))

        # positions
        self.pos_x = (pygame.display.get_surface().get_width() - self.rect.width) / 2
        self.goal_pos_y = pos_y
        self.pos_y = 0 - self.font_rect.height
        self.pos_start = self.pos_y

        # fading and display time
        self.timer = pygame.time.Clock()
        self.time = 0
        self.display_time = display_time
        self.fade_in = True
        self.fade_out = False

    def update(self):
        # needs to be called every frame to drop time while fading
        time = self.timer.tick()
        # if fading change position, if not display for some time and kill it
        if self.fade_in:
            if self.pos_y < self.goal_pos_y:
                self.pos_y += 1
            else:
                self.fade_in = False
        elif self.fade_out:
            if self.pos_y > self.pos_start:
                self.pos_y -= 1
            else:
                self.kill()
        elif self.time >= self.display_time:
            self.fade_out = True
        else:
            self.time += time
        # move the box
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y


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


class MessageBoxRecty(Form):
    def __init__(self, rect: pygame.Rect, color) -> None:
        Form.__init__(self, rect.size)

        self.pos_x = rect.x
        self.pos_y = rect.y
        self.rect = rect
        self.image.fill(color)

    def update(self) -> None:
        pass


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
        button_width = 70
        button_height = 24
        button_padding = 5
        border_width = 5

        # colors
        border_color = COLOR_BLACK
        text_rect_color = COLOR_GRAY
        text_color = COLOR_WHITE
        caption_color = COLOR_WHITE

        # create labels
        self.text = Label((0, 0), text)
        self.text.set_font(False, MSG_FONT_SIZE)
        self.text.font_color(caption_color)
        text_width, text_height = self.text.rect.size

        self.caption = Label((0, 0), caption)
        self.caption.set_font(False, MSG_FONT_SIZE)
        self.caption.font_color(text_color)
        caption_width, caption_height = self.caption.rect.size

        # calc title size
        title_height = 3 * border_width + caption_height + text_height + 2 * button_padding + button_height
        title_width_1 = 2 * border_width + caption_width
        title_width_2 = 2 * border_width + text_width
        title_width_3 = 2 * border_width + 3 * button_padding + 2 * button_width
        title_width = max([title_width_1, title_width_2, title_width_3])

        self.title_rect = pygame.Rect(((pygame.display.get_surface().get_width() - title_width) // 2,
                                       (pygame.display.get_surface().get_height() - title_height) // 2),
                                      (title_width, title_height))

        # create title
        self.title = Title(self.title_rect, border_color)
        self.title.set_alpha(255)

        # fit labels onto title
        self.caption.pos_x = title_width // 2
        self.caption.pos_y = border_width
        self.text.pos_x = title_width // 2
        self.text.pos_y = 2 * border_width + caption_height
        self.caption.align(CENTER)
        self.text.align(CENTER)

        # create a colored rect as background
        self.text_surface = MessageBoxRecty(pygame.Rect(
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
            b_yes.set_font(False, 13)
            b_yes.align(LEFT)

            b_no = Button(
                pygame.Rect((title_width - border_width - button_padding,
                             title_height - border_width - button_padding - button_height),
                            (button_width, button_height)),
                btn_no.sprite_sheet_handler,
                btn_no.sprite_sheet_key,
                btn_no.text,
                btn_no.event
            )
            b_no.set_font(False, 13)
            b_no.align(RIGHT)
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
            b_yes.set_font(False, 13)
            b_yes.align(CENTER)

        # add everything to the title
        self.title.add(self.text_surface)
        self.title.add([self.caption, self.text, b_yes])
        if btn_no is not None:
            self.title.add(b_no)


class MessageHandler(object):
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
