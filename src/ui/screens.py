import pygame
import src.ui.form as forms
import src.locales as locales


class GamePausedScreen(forms.Interface):
    def __init__(self, rect):
        super().__init__()

        self.rect = rect
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self._text = f"{locales.get('info_game_paused')}"

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(forms.ALPHA)

        l_paused = forms.Label((self.title.width() // 2, self.title.height() // 2), self.text, 20)
        l_paused.font_color(forms.COLOR_WHITE)
        l_paused.align(forms.CENTER)

        self.title.add(l_paused)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value


class GameLoadScreen(forms.Interface):
    def __init__(self, cb=None):
        super().__init__()

        self.rect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self._text = f"{locales.get('info_loading_screen')}"

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        tf_load_screen = forms.Label((self.title.width() // 2, self.title.height() // 2), self.text, 20, cb)
        tf_load_screen.font_color(forms.COLOR_WHITE)
        tf_load_screen.align(forms.CENTER)

        self.title.add(tf_load_screen)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self.text = value


class DebugScreen(forms.Interface):
    def __init__(self):
        super().__init__()

        self.clock = pygame.time.Clock()

        self.name = 'debug'
        self.rect = pygame.Rect((0, 0), (pygame.display.get_surface().get_width() // 3,
                                pygame.display.get_surface().get_height()))
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self.alpha = 192

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(self.alpha)

        self._timer = '00:00:00'

        tf_title = forms.Label((15, 40), locales.get('info_debug_title'), 18)
        tf_title.font_color(forms.COLOR_WHITE)
        tf_title.align(forms.LEFT)
        self._y = tf_title.pos_y + tf_title.height() + 10

        tf_playtime = forms.Label((15, self._y), f"{locales.get('info_play_time')}: {self.timer}",
                                  14, self.__update_timer)
        tf_playtime.font_color(forms.COLOR_WHITE)
        tf_playtime.align(forms.LEFT)

        self._y = tf_playtime.pos_y + tf_playtime.height() + 10

        self.title.add(tf_title)
        self.title.add(tf_playtime)

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value: int):
        self._timer = self.seconds_to_clock(value)

    def add(self, desc: str, callback):
        new_label = forms.Label((15, self._y), f'{desc}:', 14, lambda: self.__callback(desc, callback))
        new_label.font_color(forms.COLOR_WHITE)
        new_label.align(forms.LEFT)
        self.title.add(new_label)

        self._y = new_label.pos_y + new_label.height() + 10

    def __callback(self, text, func):
        return f'{text}: {func()}'

    def __update_timer(self):
        return f"{locales.get('info_play_time')}: {self.timer}"

    @staticmethod
    def seconds_to_clock(seconds: int):
        """ Transforms seconds into time string

        :param seconds: seconds to transform
        :returns: clock format like '00:00:00'
        """
        seconds = abs(seconds)
        hours = seconds // 3600
        minutes = (seconds - (hours * 3600)) // 60
        seconds -= (seconds - (hours * 3600)) - (seconds - (minutes * 60))

        if hours < 10:
            hours = "0" + str(hours)
        else:
            hours = str(hours)
        if minutes < 10:
            minutes = "0" + str(minutes)
        else:
            minutes = str(minutes)
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)

        return f'{hours}:{minutes}:{seconds}'
