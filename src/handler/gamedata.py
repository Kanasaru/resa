""" This module provides game src handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
from ast import literal_eval
import configparser
import pygame


class GameDataHandler(object):
    def __init__(self) -> None:
        """ Creates a game src handler """
        self._resources = {
            "Wood": 0,
            "Stone": 0,
            "Marble": 0,
            "Tools": 0,
            "Gold": 0,
        }
        self._world_data = None
        self._game_time = 0
        self._game_timer = None
        self._game_time_speed = 1
        self._pause_timer = False

    @property
    def game_time_speed(self) -> int:
        return self._game_time_speed

    @game_time_speed.setter
    def game_time_speed(self, value: int) -> None:
        if value >= 1:
            self._game_time_speed = value
        else:
            raise ValueError("Game time speed must be 1 or higher.")

    @property
    def resources(self) -> dict:
        return self._resources

    @resources.setter
    def resources(self, res: dict) -> None:
        for key, value in res.items():
            if key in self._resources:
                self._resources[key] = int(value)
            else:
                raise KeyError(f"'{key}' with '{value}' not in resources")

    @property
    def game_time(self) -> int:
        return self._game_time

    @game_time.setter
    def game_time(self, time: int) -> None:
        self._game_time = time

    def start_timer(self):
        self._game_timer = pygame.time.Clock()

    def pause_ingame_time(self):
        self._pause_timer = not self._pause_timer

    def get_game_time(self) -> str:
        """ Returns the in-game time.

        :return: in-game time
        """
        time = ((self.game_time // 1000) * self.game_time_speed)
        year = time // (365 * 24 * 3600)
        time -= year * (365 * 24 * 3600)
        day = time // (24 * 3600)
        time -= day * (24 * 3600)
        hour = time // 3600
        return f'Year {year} Day {day} Hour {hour}'

    def get_game_time_diff(self, time, count: str = 'ydh') -> tuple:
        """ Returns the in-game time.

        :return: in-game time
        """
        time = ((self.game_time // 1000) * self.game_time_speed) - time
        if count == 'ydh':
            year = time // (365 * 24 * 3600)
            time -= year * (365 * 24 * 3600)
            day = time // (24 * 3600)
            time -= day * (24 * 3600)
            hour = time // 3600
            return year, day, hour
        elif count == 'dh':
            day = time // (24 * 3600)
            time -= day * (24 * 3600)
            hour = time // 3600
            return day, hour
        elif count == 'h':
            hour = time // 3600
            return hour

    @property
    def world_data(self) -> tuple[pygame.Rect, dict, dict]:
        return self._world_data

    @world_data.setter
    def world_data(self, data: tuple[pygame.Rect, dict, dict]) -> None:
        self._world_data = data

    def update(self) -> None:
        """ Updates the handler information.

        :return: None
        """
        if self._game_timer is not None:
            self._game_timer.tick()
            if not self._pause_timer:
                self.game_time += self._game_timer.get_time()


class Settings(object):
    def __init__(self) -> None:
        """ Provides standard game settings and consts """
        self.parser = configparser.ConfigParser()

        # information
        self.title = 'Resa'
        self.version = '0.7.0-alpha'
        self.author = 'Kanasaru'
        self.www = 'bitbyteopen.org'

        # display settings
        self.icon = 'res/images/icon.png'
        self.fps = 60
        self.fullscreen = False
        self.grid_zoom = 20
        self.background_image = None
        self.map_border_thickness = 5

        # standard game values
        self.game_speed = 1440
        self.map_pace = 10
        self.save_file = 'data/saves/game.xml'
        self.std_font = None
        self.std_font_size = 20
        self.msg_font_size = 16
        self.volume = .2
        self.bg_music = None
        self.sounds = 'res/sounds'
        self.screenshot_path = 'data/saves/'
        self.autosave = False
        self.autosave_interval = 240000

        # sprite sheets
        self.sp_menu_btn_key = None
        self.sp_menu_btn = None
        self.sp_menu_btn_size = None
        self.sp_menu_swt_key = None
        self.sp_menu_swt = None
        self.sp_menu_swt_size = None
        self.sp_world = None

        # spawn rates
        self.tree_spawn_bl = 50
        self.tree_spawn_eg = 70
        self.tree_spawn_p = 35
        self.fish_spawn = 15
        self.rock_spawn = 5
        self.mountain_spawn = {
            'North_West': {0: 100, 1: 80, 2: 50},
            'North': {0: 100, 1: 80, 2: 50},
            'North_East': {0: 100, 1: 80, 2: 50},
            'Center_West': {0: 100, 1: 80, 2: 50},
            'Center': {0: 100, 1: 80, 2: 50},
            'Center_East': {0: 100, 1: 80, 2: 50},
            'South_West': {0: 100, 1: 80, 2: 50},
            'South': {0: 100, 1: 80, 2: 50},
            'South_East': {0: 100, 1: 80, 2: 50},
        }
        self.mountain_ore_spawn = {
            'North_West': {'Gold': 75, 'Iron': 100, 'Gems': 10},
            'North': {'Gold': 75, 'Iron': 100, 'Gems': 10},
            'North_East': {'Gold': 75, 'Iron': 100, 'Gems': 10},
            'Center_West': {'Gold': 50, 'Iron': 100, 'Gems': 0},
            'Center': {'Gold': 50, 'Iron': 100, 'Gems': 0},
            'Center_East': {'Gold': 50, 'Iron': 100, 'Gems': 0},
            'South_West': {'Gold': 90, 'Iron': 20, 'Gems': 70},
            'South': {'Gold': 90, 'Iron': 20, 'Gems': 70},
            'South_East': {'Gold': 90, 'Iron': 20, 'Gems': 70},
        }

        # islands max mountain
        self.max_mountain = {
            'North_West': {0: 3, 1: 2, 2: 1},
            'North': {0: 3, 1: 2, 2: 1},
            'North_East': {0: 3, 1: 2, 2: 1},
            'Center_West': {0: 3, 1: 2, 2: 1},
            'Center': {0: 3, 1: 2, 2: 1},
            'Center_East': {0: 3, 1: 2, 2: 1},
            'South_West': {0: 3, 1: 2, 2: 1},
            'South': {0: 3, 1: 2, 2: 1},
            'South_East': {0: 3, 1: 2, 2: 1},
        }

        # islands temperatures
        self.temp_north = -20
        self.temp_center = 20
        self.temp_south = 40

        # tree growth
        self.tree_growth = 36
        self.tree_grow = (50, 20, 30)

        # standard colors
        self.COLOR_KEY = (1, 0, 0)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_YELLOW = (255, 255, 0)
        self.COLOR_CYAN = (0, 255, 255)
        self.COLOR_GRAY = (128, 128, 128)
        self.COLOR_GREEN = (0, 128, 0)

    def load_config_file(self, filepath: str) -> None:
        """ Loads settings from file and replaces standard value

        :param filepath: config filepath
        :return: None
        """
        self.parser.read(filepath)

        self.background_image = self.parser.get('Screen', 'BackgroundImage')
        self.save_file = self.parser.get('GameSettings', 'SaveFile')
        self.bg_music = self.parser.get('Music', 'BackgroundMusic')
        self.volume = self.parser.getfloat('Music', 'StartVolume')

    def load_sprite_file(self, filepath: str) -> None:
        """ Loads sprite sheets from config file

        :param filepath: sprite sheet config filepath
        :return: None
        """
        self.parser.read(filepath)

        self.sp_menu_btn_key = self.parser.get('Buttons', 'MenuButtonsKey')
        self.sp_menu_btn = self.parser.get('Buttons', 'MenuButtons')
        self.sp_menu_btn_size = literal_eval(self.parser.get('Buttons', 'MenuButtonsSize'))
        self.sp_menu_swt_key = self.parser.get('Switches', 'MenuSwitchesKey')
        self.sp_menu_swt = self.parser.get('Switches', 'MenuSwitches')
        self.sp_menu_swt_size = literal_eval(self.parser.get('Switches', 'MenuSwitchesSize'))
        self.sp_world = {
            self.parser.get('Objects', 'TilesID'): (
                self.parser.get('Objects', 'TilesSheet'),
                literal_eval(self.parser.get('Objects', 'TilesSize'))),
            self.parser.get('Entities', 'TreesID'): (
                self.parser.get('Entities', 'TreesSheet'),
                literal_eval(self.parser.get('Entities', 'TreesSize'))),
            self.parser.get('Entities', 'FishesID'): (
                self.parser.get('Entities', 'FishesSheet'),
                literal_eval(self.parser.get('Entities', 'FishesSize'))),
            self.parser.get('Entities', 'RocksID'): (
                self.parser.get('Entities', 'RocksSheet'),
                literal_eval(self.parser.get('Entities', 'RocksSize'))),
            self.parser.get('Entities', 'MountainID'): (
                self.parser.get('Entities', 'MountainSheet'),
                literal_eval(self.parser.get('Entities', 'MountainSize')))
        }
